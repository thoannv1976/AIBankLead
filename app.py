"""BankLead AI - Main Dashboard (Page 1).

Run with:  streamlit run app.py
"""

import streamlit as st

from src import config, ui

ui.setup_page("Dashboard", icon="🏦")

ui.hero("BankLead AI", ui.T("dash.subtitle"))

# ---------------------------------------------------------------------------
# Intro + research objective
# ---------------------------------------------------------------------------
left, right = st.columns([2, 1])
with left:
    st.subheader(ui.T("dash.about_title"))
    st.write(ui.T("dash.about_body"))
    st.info(ui.T("dash.research_objective"))
    st.markdown(ui.T("dash.workflow"))

with right:
    st.subheader(ui.T("dash.pages_title"))
    st.markdown(ui.T("dash.pages_list"))
    st.caption(ui.T("dash.nav_caption"))

st.divider()

# ---------------------------------------------------------------------------
# Status KPIs
# ---------------------------------------------------------------------------
st.subheader(ui.T("dash.status_title"))

raw_df = st.session_state.get("raw_df")
overview = st.session_state.get("overview")
models = st.session_state.get("models")
best = st.session_state.get("best_model")

c1, c2, c3, c4 = st.columns(4)

c1.metric(ui.T("metric.customers_uploaded"),
          f"{len(raw_df):,}" if raw_df is not None else "—")

if overview and overview.get("has_target"):
    c2.metric(ui.T("metric.acceptance"), f"{overview['acceptance_rate']:.1%}")
else:
    c2.metric(ui.T("metric.acceptance"), "—")

c3.metric(ui.T("metric.models_trained"), f"{len(models)}" if models else "0")
c4.metric(ui.T("metric.best_model"), best if best else ui.T("val.not_trained"))

st.divider()

# Status guidance
if raw_df is None:
    st.warning(ui.T("dash.status_need_upload"))
elif not models:
    st.info(ui.T("dash.status_need_train"))
elif st.session_state.get("lead_df") is None:
    st.info(ui.T("dash.status_need_score"))
else:
    st.success(ui.T("dash.status_complete"))

st.caption(ui.T("dash.priority_caption", high=config.HIGH_THRESHOLD,
                med=config.MEDIUM_THRESHOLD,
                high_minus=config.HIGH_THRESHOLD - 0.01))
