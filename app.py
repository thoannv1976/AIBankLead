"""BankLead AI - Main Dashboard (Page 1).

Run with:  streamlit run app.py
"""

import streamlit as st

from src import config, ui

ui.setup_page("Dashboard", icon="🏦")

ui.hero(
    "BankLead AI",
    "AI-driven customer analytics to identify high-potential personal-loan "
    "leads from banking profile data.",
)

# ---------------------------------------------------------------------------
# Intro + research objective
# ---------------------------------------------------------------------------
left, right = st.columns([2, 1])
with left:
    st.subheader("About this app")
    st.write(
        "BankLead AI helps retail-banking marketing teams move from mass "
        "marketing to **data-driven targeting**. Instead of offering personal "
        "loans to everyone, the bank can rank customers by an AI **lead score** "
        "and focus on the most promising segments."
    )
    st.info(
        "**Research objective** — *AI-based customer analytics for potential "
        "customer identification in banking using customer profile data.*"
    )
    st.markdown(
        "**Workflow**\n"
        "1. Upload customer CSV → 2. Auto preprocess → 3. Train models "
        "(Logistic Regression, Random Forest, XGBoost) → 4. Evaluate → "
        "5. Score & rank leads → 6. Export for CRM."
    )

with right:
    st.subheader("Pages")
    st.markdown(
        "- 📤 **Upload & Preview**\n"
        "- 🤖 **Train & Evaluate**\n"
        "- 🎯 **Lead Scoring**\n"
        "- 📊 **Customer Insights**\n"
        "- 📥 **Export Results**"
    )
    st.caption("Use the sidebar to navigate between pages.")

st.divider()

# ---------------------------------------------------------------------------
# Status KPIs
# ---------------------------------------------------------------------------
st.subheader("Current session status")

raw_df = st.session_state.get("raw_df")
overview = st.session_state.get("overview")
models = st.session_state.get("models")
best = st.session_state.get("best_model")

c1, c2, c3, c4 = st.columns(4)

if raw_df is not None:
    c1.metric("Customers uploaded", f"{len(raw_df):,}")
else:
    c1.metric("Customers uploaded", "—")

if overview and overview.get("has_target"):
    c2.metric("Personal-loan acceptance", f"{overview['acceptance_rate']:.1%}")
else:
    c2.metric("Personal-loan acceptance", "—")

if models:
    c3.metric("Models trained", f"{len(models)}")
else:
    c3.metric("Models trained", "0")

c4.metric("Best model", best if best else "Not trained")

st.divider()

# Status guidance
if raw_df is None:
    st.warning("👉 Start by going to **Upload & Preview** to load a customer CSV "
               "(or click *Load sample dataset* there).")
elif not models:
    st.info("✅ Data loaded. Next, open **Train & Evaluate** to train the models.")
elif not st.session_state.get("lead_df") is not None:
    st.info("✅ Models trained. Open **Lead Scoring** to rank your customers.")
else:
    st.success("✅ Pipeline complete. Visit **Lead Scoring**, **Customer "
               "Insights**, and **Export Results**.")

st.caption(
    f"Priority bands — High: score ≥ {config.HIGH_THRESHOLD:.2f} · "
    f"Medium: {config.MEDIUM_THRESHOLD:.2f}–{config.HIGH_THRESHOLD-0.01:.2f} · "
    f"Low: < {config.MEDIUM_THRESHOLD:.2f}"
)
