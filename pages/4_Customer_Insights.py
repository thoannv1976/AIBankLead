"""Page 5: Customer Insights - feature importance, segments, recommendations."""

import plotly.express as px
import streamlit as st

from src import config, modeling, scoring, ui

ui.setup_page("Customer Insights", icon="📊")
ui.hero("Customer Insights", "Understand the drivers of conversion and profile "
        "your highest-value leads.")

ui.require_models()
if st.session_state.get("lead_df") is None:
    st.info("Open **Lead Scoring** first to generate the lead table.")
    st.stop()

data = st.session_state.data
models = st.session_state.models
lead_df = st.session_state.lead_df

# ---------------------------------------------------------------------------
# Feature importance
# ---------------------------------------------------------------------------
st.subheader("Feature importance")
model_names = list(models.keys())
default_idx = model_names.index(st.session_state.get("active_model", model_names[0])) \
    if st.session_state.get("active_model") in model_names else 0
fi_model = st.selectbox("Model", model_names, index=default_idx)

imp = modeling.feature_importance(models[fi_model], fi_model,
                                  data["feature_names"])
imp_display = imp.copy()
imp_display["feature"] = imp_display["feature"].map(
    lambda f: config.FEATURE_LABELS.get(f, f))

if fi_model == "Logistic Regression":
    fig = px.bar(imp_display.sort_values("coefficient"),
                 x="coefficient", y="feature", orientation="h",
                 color="direction",
                 color_discrete_map={"increases": config.COLORS["high"],
                                     "decreases": config.COLORS["danger"]},
                 title="Coefficient direction & magnitude")
    fig.update_layout(height=420, margin=dict(t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Positive (green) coefficients push a customer **toward** "
               "accepting a loan; negative (red) push away. Magnitude = "
               "relative influence (features are standardized).")
else:
    fig = px.bar(imp_display.sort_values("importance").tail(12),
                 x="importance", y="feature", orientation="h",
                 color_discrete_sequence=[config.COLORS["primary"]],
                 title="Relative feature importance")
    fig.update_layout(height=420, margin=dict(t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Higher bars contribute more to the model's predictions.")

st.divider()

# ---------------------------------------------------------------------------
# Segment summary
# ---------------------------------------------------------------------------
st.subheader("High-priority lead profile")
summary = scoring.segment_summary(lead_df)

if summary["n_high"] == 0:
    st.info("No high-priority leads (score ≥ 0.70) in this dataset/model.")
else:
    g1, g2, g3, g4 = st.columns(4)
    g1.metric("High-priority leads", f"{summary['n_high']:,}")
    if summary["avg_income_high"] == summary["avg_income_high"]:
        g2.metric("Avg income (high)", f"${summary['avg_income_high']:.0f}k",
                  delta=f"{summary['avg_income_high']-summary['avg_income_base']:+.0f}k vs base")
    if summary["avg_ccavg_high"] == summary["avg_ccavg_high"]:
        g3.metric("Avg card spend (high)", f"${summary['avg_ccavg_high']:.1f}k")
    if summary["avg_mortgage_high"] == summary["avg_mortgage_high"]:
        g4.metric("Avg mortgage (high)", f"${summary['avg_mortgage_high']:.0f}k")

    r1, r2, r3 = st.columns(3)
    if "online_rate_high" in summary:
        r1.metric("Use online banking", f"{summary['online_rate_high']:.0%}")
    if "cd_rate_high" in summary:
        r2.metric("Hold a CD account", f"{summary['cd_rate_high']:.0%}")
    if "cc_rate_high" in summary:
        r3.metric("Own a credit card", f"{summary['cc_rate_high']:.0%}")

    if "education_dist_high" in summary:
        st.markdown("**Education distribution (high-priority leads)**")
        edu_map = {1: "Undergrad", 2: "Graduate", 3: "Advanced/Pro"}
        edu = summary["education_dist_high"].rename(index=edu_map).reset_index()
        edu.columns = ["Education", "Share"]
        fig = px.pie(edu, names="Education", values="Share", hole=0.45,
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        fig.update_layout(height=320, margin=dict(t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# Campaign recommendations
# ---------------------------------------------------------------------------
st.subheader("📌 Campaign recommendations")
for rec in scoring.campaign_recommendations(lead_df, summary):
    st.markdown(f"- {rec}")
