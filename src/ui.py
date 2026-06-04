"""Shared Streamlit UI helpers: theming, headers, language, priority badges."""

from __future__ import annotations

import streamlit as st

from . import config, i18n

CUSTOM_CSS = f"""
<style>
    .main {{ background-color: {config.COLORS['white']}; }}
    h1, h2, h3 {{ color: {config.COLORS['primary']}; }}
    .bl-hero {{
        background: linear-gradient(120deg, {config.COLORS['primary']} 0%,
                    {config.COLORS['primary_light']} 100%);
        padding: 1.4rem 1.8rem; border-radius: 14px; color: white;
        margin-bottom: 1.2rem;
    }}
    .bl-hero h1 {{ color: white !important; margin: 0; font-size: 1.9rem; }}
    .bl-hero p {{ color: #DCE6F7; margin: 0.4rem 0 0 0; font-size: 1rem; }}
    .bl-pill {{
        display: inline-block; padding: 0.15rem 0.7rem; border-radius: 999px;
        font-size: 0.8rem; font-weight: 600; color: white;
    }}
    div[data-testid="stMetric"] {{
        background: {config.COLORS['light_grey']};
        border: 1px solid #E3E8F0; border-radius: 12px;
        padding: 0.8rem 1rem;
    }}
</style>
"""


# ---------------------------------------------------------------------------
# Language helpers
# ---------------------------------------------------------------------------
def get_lang() -> str:
    """Current UI language code ('en' or 'vi'); defaults to Vietnamese."""
    return st.session_state.get("lang", i18n.DEFAULT_LANG)


def T(key: str, **kwargs) -> str:
    """Translate a key into the current session language."""
    return i18n.t(key, get_lang(), **kwargs)


def language_selector():
    """Render the language picker at the top of the sidebar (all pages)."""
    with st.sidebar:
        codes = list(i18n.LANGUAGES.keys())
        current = get_lang()
        idx = codes.index(current) if current in codes else 0
        choice = st.radio(
            i18n.t("language_label", current),
            codes, index=idx, horizontal=True,
            format_func=lambda c: i18n.LANGUAGES[c], key="lang",
        )
        st.divider()
        return choice


def setup_page(title: str, icon: str = "🏦"):
    """Apply page config + global CSS + language selector. Call once per page."""
    st.set_page_config(page_title=f"BankLead AI - {title}", page_icon=icon,
                       layout="wide", initial_sidebar_state="expanded")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    language_selector()


def hero(title: str, subtitle: str):
    """Render the gradient hero header."""
    st.markdown(
        f"<div class='bl-hero'><h1>{title}</h1><p>{subtitle}</p></div>",
        unsafe_allow_html=True,
    )


def priority_badge(priority: str) -> str:
    """Return an HTML pill for a priority band (accepts localized label)."""
    lang = get_lang()
    color_map = i18n.priority_color_map(lang, config.COLORS)
    color = color_map.get(priority, config.COLORS["grey"])
    return f"<span class='bl-pill' style='background:{color}'>{priority}</span>"


def style_lead_table(df):
    """Color the (localized) Priority column and format Lead Score.

    ``df`` is expected to already have localized column headers/values.
    """
    lang = get_lang()
    priority_col = i18n.header_label("Priority", lang)
    score_col = i18n.header_label("Lead Score", lang)
    color_map = i18n.priority_color_map(lang, config.COLORS)

    def color_priority(val):
        color = color_map.get(val, "#FFFFFF")
        return f"background-color: {color}; color: white; font-weight:600;"

    styler = df.style
    if priority_col in df.columns:
        styler = styler.map(color_priority, subset=[priority_col])
    if score_col in df.columns:
        styler = styler.format({score_col: "{:.3f}"})
    return styler


def require_data():
    """Guard: stop the page if no dataset is loaded yet."""
    if "raw_df" not in st.session_state or st.session_state.raw_df is None:
        st.warning(T("guard.no_data"))
        st.stop()


def require_models():
    """Guard: stop the page if models haven't been trained."""
    require_data()
    if not st.session_state.get("models"):
        st.warning(T("guard.no_models"))
        st.stop()
