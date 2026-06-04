"""Page 2: Upload Data & Preview."""

import os

import plotly.express as px
import streamlit as st

from src import config, preprocessing, ui

ui.setup_page("Upload & Preview", icon="📤")
ui.hero("Upload & Preview", "Load a customer CSV and inspect it before training.")

SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "sample_data",
                           "bank_customers_sample.csv")


def _store(df):
    st.session_state.raw_df = df
    st.session_state.overview = preprocessing.data_overview(df)
    # Invalidate any downstream artefacts from a previous dataset.
    for key in ("data", "models", "test_scores", "results", "best_model",
                "lead_df", "active_model"):
        st.session_state.pop(key, None)


# ---------------------------------------------------------------------------
# Upload controls
# ---------------------------------------------------------------------------
col_up, col_sample = st.columns([3, 1])
with col_up:
    uploaded = st.file_uploader(
        "Upload customer profile CSV", type=["csv"],
        help="Expected columns include Age, Income, Family, CCAvg, Education, "
             "Mortgage, CD Account, Online, CreditCard and the target "
             "'Personal Loan'.",
    )
    if uploaded is not None:
        try:
            df = preprocessing.load_csv(uploaded)
            _store(df)
            st.success(f"Loaded **{uploaded.name}** — {len(df):,} rows.")
        except Exception as e:
            st.error(f"Could not read CSV: {e}")

with col_sample:
    st.write("")
    st.write("")
    if st.button("📥 Load sample dataset", use_container_width=True):
        if os.path.exists(SAMPLE_PATH):
            df = preprocessing.load_csv(SAMPLE_PATH)
            _store(df)
            st.success(f"Sample dataset loaded — {len(df):,} rows.")
        else:
            st.error("Sample file not found. Run "
                     "`python sample_data/generate_sample.py` first.")

# ---------------------------------------------------------------------------
# Preview & summary
# ---------------------------------------------------------------------------
if st.session_state.get("raw_df") is None:
    st.info("Upload a CSV or load the sample dataset to continue.")
    st.stop()

df = st.session_state.raw_df
overview = st.session_state.overview

st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Customer records", f"{overview['n_rows']:,}")
c2.metric("Variables", overview["n_cols"])
c3.metric("Missing values", f"{overview['missing_total']:,}")
if overview.get("has_target"):
    c4.metric("Acceptance rate", f"{overview['acceptance_rate']:.1%}")
else:
    c4.metric("Acceptance rate", "no target")

if not overview.get("has_target"):
    st.warning(f"⚠️ Target column **'{config.TARGET}'** not detected. Training "
               "requires a personal-loan label (1 = accepted, 0 = not).")

st.subheader("Data preview")
st.dataframe(df.head(15), use_container_width=True)

# Missing-value summary
st.subheader("Missing values")
if overview["missing_total"] == 0:
    st.success("No missing values detected. 🎉")
else:
    miss = overview["missing_by_col"].rename("missing").reset_index()
    miss.columns = ["column", "missing"]
    st.dataframe(miss, use_container_width=True, hide_index=True)

# Target distribution
if overview.get("has_target"):
    st.subheader("Target distribution — Personal Loan")
    counts = overview["target_counts"]
    cc1, cc2 = st.columns([1, 2])
    with cc1:
        st.metric("Accepted (1)", f"{overview['n_accepted']:,}")
        st.metric("Not accepted (0)",
                  f"{overview['n_rows'] - overview['n_accepted']:,}")
    with cc2:
        label_map = {0: "Not accepted (0)", 1: "Accepted (1)"}
        plot_df = counts.rename(index=label_map).reset_index()
        plot_df.columns = ["Personal Loan", "Customers"]
        fig = px.bar(
            plot_df, x="Personal Loan", y="Customers", text="Customers",
            color="Personal Loan",
            color_discrete_map={"Accepted (1)": config.COLORS["high"],
                                "Not accepted (0)": config.COLORS["grey"]},
        )
        fig.update_layout(showlegend=False, height=320,
                          margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)
    st.caption("Personal-loan acceptance is typically imbalanced — the app "
               "handles this with balanced class weights / scale_pos_weight.")

st.success("Data ready. Proceed to **Train & Evaluate**.")
