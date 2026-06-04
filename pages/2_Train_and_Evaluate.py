"""Page 3: Train Models & Evaluation Dashboard."""

import pandas as pd
import plotly.express as px
import streamlit as st

from src import config, metrics, modeling, preprocessing, ui

ui.setup_page("Train & Evaluate", icon="🤖")
ui.hero(ui.T("train.title"), ui.T("train.subtitle"))

ui.require_data()

overview = st.session_state.overview
if not overview.get("has_target"):
    st.error(ui.T("train.need_target_error", target=config.TARGET))
    st.stop()

# ---------------------------------------------------------------------------
# Controls
# ---------------------------------------------------------------------------
available = list(config.MODEL_NAMES)
if not modeling.HAS_XGB and "XGBoost" in available:
    available.remove("XGBoost")
    st.caption(ui.T("train.xgb_missing_caption"))

c1, c2 = st.columns([3, 1])
with c1:
    chosen = st.multiselect(ui.T("train.models_to_train"), available,
                            default=available)
with c2:
    test_size = st.slider(ui.T("train.test_size"), 0.1, 0.4, 0.25, 0.05)

if st.button(ui.T("train.train_btn"), type="primary", use_container_width=True):
    if not chosen:
        st.warning(ui.T("train.select_one"))
    else:
        with st.spinner(ui.T("train.spinner")):
            data = preprocessing.preprocess(st.session_state.raw_df,
                                            test_size=test_size)
            models, test_scores, results = modeling.train_all(data, chosen)
            st.session_state.data = data
            st.session_state.models = models
            st.session_state.test_scores = test_scores
            st.session_state.results = results
            st.session_state.best_model = metrics.best_model(results)
            st.session_state.active_model = st.session_state.best_model
            # New training invalidates an old lead table.
            st.session_state.pop("lead_df", None)
        dropped = data["dropped_columns"] or ui.T("val.none")
        if isinstance(dropped, list):
            dropped = ", ".join(dropped)
        st.success(ui.T("train.trained_success", n=len(models), dropped=dropped))

# ---------------------------------------------------------------------------
# Results dashboard
# ---------------------------------------------------------------------------
results = st.session_state.get("results")
if not results:
    st.info(ui.T("train.info_configure"))
    st.stop()

best = st.session_state.best_model
st.divider()
st.subheader(ui.T("train.best_model_title"))
st.markdown(
    f"<span class='bl-pill' style='background:{config.COLORS['high']};"
    f"font-size:1rem'>{best}</span>", unsafe_allow_html=True)
st.caption(ui.T("train.best_caption"))

# Metrics table
metric_order = [
    "Accuracy", "Precision", "Recall", "F1-score", "ROC-AUC", "PR-AUC",
    "Precision@Top 5%", "Precision@Top 10%", "Precision@Top 20%",
    "Lift@Top 5%", "Lift@Top 10%", "Lift@Top 20%",
]
table = pd.DataFrame(results).T[metric_order]

st.subheader(ui.T("train.perf_comparison"))

def _highlight_best(col):
    is_max = col == col.max()
    return [f"background-color: {config.COLORS['high']}; color:white"
            if v else "" for v in is_max]

fmt = {m: "{:.3f}" for m in metric_order if not m.startswith("Lift")}
fmt.update({m: "{:.2f}×" for m in metric_order if m.startswith("Lift")})
st.dataframe(table.style.apply(_highlight_best, axis=0).format(fmt),
             use_container_width=True)

# Visual comparisons
st.subheader(ui.T("train.visual_comparison"))
tab1, tab2 = st.tabs([ui.T("tab.core_metrics"), ui.T("tab.topk_metrics")])

with tab1:
    core = ["Precision", "Recall", "F1-score", "ROC-AUC", "PR-AUC"]
    melt = table[core].reset_index().melt(id_vars="index",
                                          var_name="Metric", value_name="Score")
    melt.columns = ["Model", "Metric", "Score"]
    fig = px.bar(melt, x="Metric", y="Score", color="Model", barmode="group",
                 color_discrete_sequence=[config.COLORS["primary"],
                                          config.COLORS["accent"],
                                          config.COLORS["medium"]])
    fig.update_layout(height=400, margin=dict(t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    prec_cols = ["Precision@Top 5%", "Precision@Top 10%", "Precision@Top 20%"]
    melt = table[prec_cols].reset_index().melt(id_vars="index",
                                               var_name="Metric", value_name="Score")
    melt.columns = ["Model", "Segment", "Precision"]
    fig = px.bar(melt, x="Segment", y="Precision", color="Model", barmode="group",
                 color_discrete_sequence=[config.COLORS["primary"],
                                          config.COLORS["accent"],
                                          config.COLORS["medium"]])
    fig.update_layout(height=400, margin=dict(t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)
    st.caption(ui.T("train.topk_caption"))

st.success(ui.T("train.eval_complete", best=best))
