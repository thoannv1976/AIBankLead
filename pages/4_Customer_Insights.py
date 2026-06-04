"""Page 5: Customer Insights - feature importance, segments, recommendations."""

import plotly.express as px
import streamlit as st

from src import config, i18n, modeling, scoring, ui

ui.setup_page("Customer Insights", icon="📊")
ui.hero(ui.T("insights.title"), ui.T("insights.subtitle"))

ui.require_models()
if st.session_state.get("lead_df") is None:
    st.info(ui.T("insights.open_scoring_info"))
    st.stop()

lang = ui.get_lang()
data = st.session_state.data
models = st.session_state.models
lead_df = st.session_state.lead_df

# ---------------------------------------------------------------------------
# Feature importance
# ---------------------------------------------------------------------------
st.subheader(ui.T("insights.feature_importance"))
model_names = list(models.keys())
default_idx = model_names.index(st.session_state.get("active_model", model_names[0])) \
    if st.session_state.get("active_model") in model_names else 0
fi_model = st.selectbox(ui.T("insights.model"), model_names, index=default_idx)

imp = modeling.feature_importance(models[fi_model], fi_model,
                                  data["feature_names"])
imp_display = imp.copy()
imp_display["feature"] = imp_display["feature"].map(
    lambda f: i18n.feature_label(f, lang))

if fi_model == "Logistic Regression":
    fig = px.bar(imp_display.sort_values("coefficient"),
                 x="coefficient", y="feature", orientation="h",
                 color="direction",
                 color_discrete_map={"increases": config.COLORS["high"],
                                     "decreases": config.COLORS["danger"]},
                 title=ui.T("chart.lr_title"))
    fig.update_layout(height=420, margin=dict(t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)
    st.caption(ui.T("insights.lr_caption"))
else:
    fig = px.bar(imp_display.sort_values("importance").tail(12),
                 x="importance", y="feature", orientation="h",
                 color_discrete_sequence=[config.COLORS["primary"]],
                 title=ui.T("chart.tree_title"))
    fig.update_layout(height=420, margin=dict(t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)
    st.caption(ui.T("insights.tree_caption"))

st.divider()

# ---------------------------------------------------------------------------
# Segment summary
# ---------------------------------------------------------------------------
st.subheader(ui.T("insights.high_profile"))
summary = scoring.segment_summary(lead_df)

if summary["n_high"] == 0:
    st.info(ui.T("insights.no_high"))
else:
    g1, g2, g3, g4 = st.columns(4)
    g1.metric(ui.T("metric.high_leads"), f"{summary['n_high']:,}")
    if summary["avg_income_high"] == summary["avg_income_high"]:
        delta = ui.T("delta.vs_base",
                     v=summary["avg_income_high"] - summary["avg_income_base"])
        g2.metric(ui.T("metric.avg_income_high"),
                  f"${summary['avg_income_high']:.0f}k", delta=delta)
    if summary["avg_ccavg_high"] == summary["avg_ccavg_high"]:
        g3.metric(ui.T("metric.avg_card_high"), f"${summary['avg_ccavg_high']:.1f}k")
    if summary["avg_mortgage_high"] == summary["avg_mortgage_high"]:
        g4.metric(ui.T("metric.avg_mortgage_high"), f"${summary['avg_mortgage_high']:.0f}k")

    r1, r2, r3 = st.columns(3)
    if "online_rate_high" in summary:
        r1.metric(ui.T("metric.use_online"), f"{summary['online_rate_high']:.0%}")
    if "cd_rate_high" in summary:
        r2.metric(ui.T("metric.hold_cd"), f"{summary['cd_rate_high']:.0%}")
    if "cc_rate_high" in summary:
        r3.metric(ui.T("metric.own_cc"), f"{summary['cc_rate_high']:.0%}")

    if "education_dist_high" in summary:
        st.markdown(ui.T("insights.edu_dist"))
        edu_map = {1: ui.T("edu.undergrad"), 2: ui.T("edu.graduate"),
                   3: ui.T("edu.advanced")}
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
st.subheader(ui.T("insights.recommendations_title"))
for rec in scoring.campaign_recommendations(lead_df, summary, lang):
    st.markdown(f"- {rec}")
