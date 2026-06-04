"""Page 4: Lead Scoring Dashboard."""

import plotly.express as px
import streamlit as st

from src import config, modeling, scoring, ui

ui.setup_page("Lead Scoring", icon="🎯")
ui.hero("Lead Scoring", "Rank every customer by predicted probability of "
        "accepting a personal-loan offer.")

ui.require_models()

# ---------------------------------------------------------------------------
# Choose scoring model and (re)build the lead table
# ---------------------------------------------------------------------------
models = st.session_state.models
model_names = list(models.keys())
default_idx = model_names.index(st.session_state.get("active_model", model_names[0])) \
    if st.session_state.get("active_model") in model_names else 0

c1, c2 = st.columns([2, 1])
with c1:
    active = st.selectbox("Scoring model", model_names, index=default_idx)
with c2:
    st.write("")
    st.write("")
    st.caption(f"Best model: **{st.session_state.best_model}**")

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
st.subheader("Lead priority overview")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total leads", f"{len(lead_df):,}")
m2.metric("🟢 High priority", f"{dist['High']:,}")
m3.metric("🟡 Medium priority", f"{dist['Medium']:,}")
m4.metric("⚪ Low priority", f"{dist['Low']:,}")

dd = dist.reset_index()
dd.columns = ["Priority", "Customers"]
fig = px.bar(dd, x="Priority", y="Customers", color="Priority", text="Customers",
             color_discrete_map=config.PRIORITY_COLORS)
fig.update_layout(showlegend=False, height=300, margin=dict(t=20, b=20))
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# Top-lead selection
# ---------------------------------------------------------------------------
st.subheader("Select top leads for your campaign")
sc1, sc2 = st.columns([2, 1])
with sc1:
    mode = st.radio("Selection mode",
                    ["Top 5%", "Top 10%", "Top 20%", "Custom count", "All leads"],
                    horizontal=True)
with sc2:
    custom_n = st.number_input("Custom count", min_value=1,
                               max_value=len(lead_df),
                               value=min(100, len(lead_df)), step=10)

frac_map = {"Top 5%": 0.05, "Top 10%": 0.10, "Top 20%": 0.20}
if mode in frac_map:
    selected = scoring.top_k_leads(lead_df, fraction=frac_map[mode])
elif mode == "Custom count":
    selected = scoring.top_k_leads(lead_df, count=int(custom_n))
else:
    selected = lead_df

st.session_state.selected_leads = selected

# Conversion within selection (if actuals available)
info1, info2, info3 = st.columns(3)
info1.metric("Selected leads", f"{len(selected):,}")
if "Actual (Personal Loan)" in selected.columns:
    captured = int(selected["Actual (Personal Loan)"].sum())
    total_pos = int(lead_df["Actual (Personal Loan)"].sum())
    info2.metric("Real converters captured", f"{captured:,}")
    if total_pos:
        info3.metric("% of all converters reached", f"{captured/total_pos:.0%}")

# ---------------------------------------------------------------------------
# Ranked lead table
# ---------------------------------------------------------------------------
st.subheader("Ranked lead list")
display_cols = ["Rank", "Customer ID", "Lead Score", "Priority"]
for c in ["Income", "Age", "Family", "CCAvg", "Education", "Mortgage",
          "CD Account", "Online", "CreditCard"]:
    if c in selected.columns:
        display_cols.append(c)
display_cols.append("Recommended Action")

show = selected[display_cols].head(500)
st.dataframe(ui.style_lead_table(show), use_container_width=True, height=460,
             hide_index=True)
if len(selected) > 500:
    st.caption(f"Showing first 500 of {len(selected):,} selected leads. "
               "Use **Export Results** to download the full list.")

st.success("Leads scored. See **Customer Insights** for drivers, or "
           "**Export Results** to download.")
