"""Lead scoring outputs: ranked table, segment summary, recommendations."""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import config, i18n


def build_lead_table(data: dict, scores: np.ndarray) -> pd.DataFrame:
    """Combine customer features with scores, priority and recommended action."""
    df = data["X"].copy().reset_index(drop=True)
    df.insert(0, "Customer ID", data["ids"].values)
    df["Lead Score"] = np.round(scores, 4)
    df["Priority"] = [config.priority_band(s) for s in scores]
    df["Recommended Action"] = [config.recommended_action(s) for s in scores]
    if config.TARGET in data["y"].index.names or True:
        df["Actual (Personal Loan)"] = data["y"].reset_index(drop=True).values
    df = df.sort_values("Lead Score", ascending=False).reset_index(drop=True)
    df.insert(1, "Rank", np.arange(1, len(df) + 1))
    return df


def top_k_leads(lead_df: pd.DataFrame, fraction: float | None = None,
                count: int | None = None) -> pd.DataFrame:
    """Return the top fraction (e.g. 0.1) or top-N leads, by rank."""
    if count is not None:
        k = min(count, len(lead_df))
    elif fraction is not None:
        k = max(1, int(round(len(lead_df) * fraction)))
    else:
        k = len(lead_df)
    return lead_df.head(k).copy()


def priority_distribution(lead_df: pd.DataFrame) -> pd.Series:
    """Count of leads in each priority band (High/Medium/Low)."""
    order = ["High", "Medium", "Low"]
    counts = lead_df["Priority"].value_counts()
    return counts.reindex(order).fillna(0).astype(int)


def _rate(series: pd.Series) -> float:
    """Share of values that are truthy (>0). Used for binary flag columns."""
    return float((series > 0).mean()) if len(series) else 0.0


def segment_summary(lead_df: pd.DataFrame) -> dict:
    """Profile high-priority leads vs. the rest of the customer base."""
    high = lead_df[lead_df["Priority"] == "High"]
    base = lead_df

    def safe_mean(df, col):
        return float(df[col].mean()) if col in df.columns and len(df) else float("nan")

    summary = {
        "n_high": len(high),
        "avg_income_high": safe_mean(high, "Income"),
        "avg_income_base": safe_mean(base, "Income"),
        "avg_ccavg_high": safe_mean(high, "CCAvg"),
        "avg_ccavg_base": safe_mean(base, "CCAvg"),
        "avg_mortgage_high": safe_mean(high, "Mortgage"),
        "avg_mortgage_base": safe_mean(base, "Mortgage"),
        "avg_family_high": safe_mean(high, "Family"),
    }
    if "CD Account" in high.columns:
        summary["cd_rate_high"] = _rate(high["CD Account"])
        summary["cd_rate_base"] = _rate(base["CD Account"])
    if "Online" in high.columns:
        summary["online_rate_high"] = _rate(high["Online"])
        summary["online_rate_base"] = _rate(base["Online"])
    if "CreditCard" in high.columns:
        summary["cc_rate_high"] = _rate(high["CreditCard"])
        summary["cc_rate_base"] = _rate(base["CreditCard"])
    if "Securities Account" in high.columns:
        summary["sec_rate_high"] = _rate(high["Securities Account"])
    if "Education" in high.columns:
        summary["education_dist_high"] = (
            high["Education"].value_counts(normalize=True).sort_index()
        )
    return summary


def campaign_recommendations(lead_df: pd.DataFrame, summary: dict,
                             lang: str = i18n.DEFAULT_LANG) -> list[str]:
    """Generate plain-language marketing recommendations (localized)."""
    dist = priority_distribution(lead_df)
    recs = [i18n.t("rec.focus_high", lang, n=int(dist["High"]),
                   thr=config.HIGH_THRESHOLD)]
    if not np.isnan(summary.get("avg_income_high", float("nan"))):
        recs.append(i18n.t("rec.personalize", lang,
                           income=summary["avg_income_high"]))
    recs.append(i18n.t("rec.nurture", lang, n=int(dist["Medium"])))
    recs.append(i18n.t("rec.avoid_low", lang, n=int(dist["Low"])))
    recs.append(i18n.t("rec.export_crm", lang))
    recs.append(i18n.t("rec.retrain", lang))
    return recs


def localize_lead_df(df: pd.DataFrame, lang: str = i18n.DEFAULT_LANG) -> pd.DataFrame:
    """Return a display copy with localized Priority/Action values & headers.

    Internal storage keeps English canonical values; this is purely cosmetic.
    """
    out = df.copy()
    if "Priority" in out.columns:
        # Derive the localized action from the (English) priority band first.
        if "Recommended Action" in out.columns:
            out["Recommended Action"] = out["Priority"].map(
                lambda b: i18n.action_label(b, lang))
        out["Priority"] = out["Priority"].map(
            lambda b: i18n.priority_label(b, lang))
    out = out.rename(columns={c: i18n.header_label(c, lang) for c in out.columns})
    return out


# Columns to keep when exporting a clean lead list for CRM use.
EXPORT_KEY_FEATURES = [
    "Age", "Income", "Family", "CCAvg", "Education",
    "Mortgage", "CD Account", "Online", "CreditCard",
]


def export_frame(lead_df: pd.DataFrame) -> pd.DataFrame:
    """Build a tidy export table: id, score, priority, key features, action."""
    cols = ["Customer ID", "Rank", "Lead Score", "Priority"]
    cols += [c for c in EXPORT_KEY_FEATURES if c in lead_df.columns]
    cols += ["Recommended Action"]
    return lead_df[cols].copy()
