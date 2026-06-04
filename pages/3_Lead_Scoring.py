"""Page 4: Lead Scoring Dashboard."""

import plotly.express as px
import streamlit as st

from src import config, i18n, modeling, scoring, ui

ui.setup_page("Lead Scoring", icon="🎯")
ui.hero(ui.T("lead.title"), ui.T("lead.subtitle"))

ui.require_models()
lang = ui.get_lang()

# ---------------------------------------------------------------------------
# Choose scoring model and (re)build the lead table
# ---------------------------------------------------------------------------
models = st.session_state.models
model_names = list(models.keys())
default_idx = model_names.index(st.session_state.get("active_model", model_names[0])) \
    if st.session_state.get("active_model") in model_names else 0

c1, c2 = st.columns([2, 1])
with c1:
    active = st.selectbox(ui.T("lead.scoring_model"), model_names, index=default_idx)
with c2:
    st.write("")
    st.write("")
    st.caption(ui.T("lead.best_model_caption", best=st.session_state.best_model))

# Rebuild the lead table whenever the active model changes.
if (st.session_state.get("active_model") != active
        or st.session_state.get("lead_df") is None):
    data = st.session_state.data
    scores = modeling.score_all_customers(models[active], active, data)
    st.session_state.lead_df = scoring.build_lead_table(data, scores)
    st.session_state.active_model = active

lead_df = st.session_state.lead_df

# ---------------------------------------------------------------------------
# Priority distribution
# ---------------------------------------------------------------------------
dist = scoring.priority_distribution(lead_df)
st.subheader(ui.T("lead.priority_overview"))
m1, m2, m3, m4 = st.columns(4)
m1.metric(ui.T("metric.total_leads"), f"{len(lead_df):,}")
m2.metric(ui.T("metric.high_priority"), f"{dist['High']:,}")
m3.metric(ui.T("metric.medium_priority"), f"{dist['Medium']:,}")
m4.metric(ui.T("metric.low_priority"), f"{dist['Low']:,}")

dd = dist.reset_index()
dd.columns = ["band", ui.T("chart.customers")]
dd["Priority"] = dd["band"].map(lambda b: i18n.priority_label(b, lang))
fig = px.bar(dd, x="Priority", y=ui.T("chart.customers"), color="Priority",
             text=ui.T("chart.customers"),
             color_discrete_map=i18n.priority_color_map(lang, config.COLORS))
fig.update_layout(showlegend=False, height=300, margin=dict(t=20, b=20))
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# Top-lead selection
# ---------------------------------------------------------------------------
st.subheader(ui.T("lead.select_title"))
sc1, sc2 = st.columns([2, 1])
with sc1:
    mode_keys = ["mode.top5", "mode.top10", "mode.top20", "mode.custom", "mode.all"]
    mode = st.radio(ui.T("lead.selection_mode"), mode_keys, horizontal=True,
                    format_func=lambda k: ui.T(k))
with sc2:
    custom_n = st.number_input(ui.T("lead.custom_count"), min_value=1,
                               max_value=len(lead_df),
                               value=min(100, len(lead_df)), step=10)

frac_map = {"mode.top5": 0.05, "mode.top10": 0.10, "mode.top20": 0.20}
if mode in frac_map:
    selected = scoring.top_k_leads(lead_df, fraction=frac_map[mode])
elif mode == "mode.custom":
    selected = scoring.top_k_leads(lead_df, count=int(custom_n))
else:
    selected = lead_df

st.session_state.selected_leads = selected

# Conversion within selection (if actuals available)
info1, info2, info3 = st.columns(3)
info1.metric(ui.T("metric.selected_leads"), f"{len(selected):,}")
if "Actual (Personal Loan)" in selected.columns:
    captured = int(selected["Actual (Personal Loan)"].sum())
    total_pos = int(lead_df["Actual (Personal Loan)"].sum())
    info2.metric(ui.T("metric.converters_captured"), f"{captured:,}")
    if total_pos:
        info3.metric(ui.T("metric.pct_converters"), f"{captured/total_pos:.0%}")

# ---------------------------------------------------------------------------
# Ranked lead table
# ---------------------------------------------------------------------------
st.subheader(ui.T("lead.ranked_list"))
display_cols = ["Rank", "Customer ID", "Lead Score", "Priority"]
for c in ["Income", "Age", "Family", "CCAvg", "Education", "Mortgage",
          "CD Account", "Online", "CreditCard"]:
    if c in selected.columns:
        display_cols.append(c)
display_cols.append("Recommended Action")

show = selected[display_cols].head(500)
show_local = scoring.localize_lead_df(show, lang)
st.dataframe(ui.style_lead_table(show_local), use_container_width=True,
             height=460, hide_index=True)
if len(selected) > 500:
    st.caption(ui.T("lead.showing_first", total=len(selected)))

st.success(ui.T("lead.success"))
