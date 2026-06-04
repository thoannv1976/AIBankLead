"""Page 2: Upload Data & Preview."""

import os

import plotly.express as px
import streamlit as st

from src import config, preprocessing, ui

ui.setup_page("Upload & Preview", icon="📤")
ui.hero(ui.T("upload.title"), ui.T("upload.subtitle"))

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
        ui.T("upload.uploader_label"), type=["csv"],
        help=ui.T("upload.uploader_help"),
    )
    if uploaded is not None:
        try:
            df = preprocessing.load_csv(uploaded)
            _store(df)
            st.success(ui.T("upload.loaded_rows", name=uploaded.name, n=len(df)))
        except Exception as e:
            st.error(ui.T("upload.read_error", err=e))

with col_sample:
    st.write("")
    st.write("")
    if st.button(ui.T("upload.load_sample_btn"), use_container_width=True):
        if os.path.exists(SAMPLE_PATH):
            df = preprocessing.load_csv(SAMPLE_PATH)
            _store(df)
            st.success(ui.T("upload.sample_loaded", n=len(df)))
        else:
            st.error(ui.T("upload.sample_not_found"))

# ---------------------------------------------------------------------------
# Preview & summary
# ---------------------------------------------------------------------------
if st.session_state.get("raw_df") is None:
    st.info(ui.T("upload.need_data_info"))
    st.stop()

df = st.session_state.raw_df
overview = st.session_state.overview

st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric(ui.T("metric.records"), f"{overview['n_rows']:,}")
c2.metric(ui.T("metric.variables"), overview["n_cols"])
c3.metric(ui.T("metric.missing_values"), f"{overview['missing_total']:,}")
if overview.get("has_target"):
    c4.metric(ui.T("metric.acceptance_short"), f"{overview['acceptance_rate']:.1%}")
else:
    c4.metric(ui.T("metric.acceptance_short"), ui.T("val.no_target"))

if not overview.get("has_target"):
    st.warning(ui.T("upload.target_warning", target=config.TARGET))

st.subheader(ui.T("upload.preview_title"))
st.dataframe(df.head(15), use_container_width=True)

# Missing-value summary
st.subheader(ui.T("upload.missing_title"))
if overview["missing_total"] == 0:
    st.success(ui.T("upload.no_missing"))
else:
    miss = overview["missing_by_col"].rename("missing").reset_index()
    miss.columns = [ui.T("upload.col_column"), ui.T("upload.col_missing")]
    st.dataframe(miss, use_container_width=True, hide_index=True)

# Target distribution
if overview.get("has_target"):
    st.subheader(ui.T("upload.target_dist_title"))
    counts = overview["target_counts"]
    cc1, cc2 = st.columns([1, 2])
    with cc1:
        st.metric(ui.T("metric.accepted"), f"{overview['n_accepted']:,}")
        st.metric(ui.T("metric.not_accepted"),
                  f"{overview['n_rows'] - overview['n_accepted']:,}")
    with cc2:
        accepted_lbl = ui.T("metric.accepted")
        not_accepted_lbl = ui.T("metric.not_accepted")
        label_map = {0: not_accepted_lbl, 1: accepted_lbl}
        plot_df = counts.rename(index=label_map).reset_index()
        plot_df.columns = ["Personal Loan", ui.T("chart.customers")]
        fig = px.bar(
            plot_df, x="Personal Loan", y=ui.T("chart.customers"),
            text=ui.T("chart.customers"), color="Personal Loan",
            color_discrete_map={accepted_lbl: config.COLORS["high"],
                                not_accepted_lbl: config.COLORS["grey"]},
        )
        fig.update_layout(showlegend=False, height=320,
                          margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)
    st.caption(ui.T("upload.imbalance_caption"))

st.success(ui.T("upload.data_ready"))
