"""Page 3: Train Models & Evaluation Dashboard."""

import pandas as pd
import plotly.express as px
import streamlit as st

from src import config, metrics, modeling, preprocessing, ui

ui.setup_page("Train & Evaluate", icon="🤖")
ui.hero("Train & Evaluate", "Train Logistic Regression, Random Forest and "
        "XGBoost, then compare them on lead-targeting metrics.")

ui.require_data()

overview = st.session_state.overview
if not overview.get("has_target"):
    st.error(f"Target column '{config.TARGET}' is required to train models.")
    st.stop()

# ---------------------------------------------------------------------------
# Controls
# ---------------------------------------------------------------------------
available = list(config.MODEL_NAMES)
if not modeling.HAS_XGB and "XGBoost" in available:
    available.remove("XGBoost")
    st.caption("ℹ️ XGBoost not installed — only Logistic Regression and "
               "Random Forest are available.")

c1, c2 = st.columns([3, 1])
with c1:
    chosen = st.multiselect("Models to train", available, default=available)
with c2:
    test_size = st.slider("Test size", 0.1, 0.4, 0.25, 0.05)

if st.button("🚀 Train models", type="primary", use_container_width=True):
    if not chosen:
        st.warning("Select at least one model.")
    else:
        with st.spinner("Preprocessing and training..."):
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
        st.success(f"Trained {len(models)} model(s). "
                   f"Dropped columns: {data['dropped_columns'] or 'none'}.")

# ---------------------------------------------------------------------------
# Results dashboard
# ---------------------------------------------------------------------------
results = st.session_state.get("results")
if not results:
    st.info("Configure and train models to see the evaluation dashboard.")
    st.stop()

best = st.session_state.best_model
st.divider()
st.subheader("🏆 Best model")
st.markdown(
    f"<span class='bl-pill' style='background:{config.COLORS['high']};"
    f"font-size:1rem'>{best}</span>", unsafe_allow_html=True)
st.caption("Selected by combined ranking on PR-AUC and top-k lead performance "
           "— the most relevant metrics for imbalanced lead identification.")

# Metrics table
metric_order = [
    "Accuracy", "Precision", "Recall", "F1-score", "ROC-AUC", "PR-AUC",
    "Precision@Top 5%", "Precision@Top 10%", "Precision@Top 20%",
    "Lift@Top 5%", "Lift@Top 10%", "Lift@Top 20%",
]
table = pd.DataFrame(results).T[metric_order]

st.subheader("Performance comparison")

def _highlight_best(col):
    is_max = col == col.max()
    return [f"background-color: {config.COLORS['high']}; color:white"
            if v else "" for v in is_max]

fmt = {m: "{:.3f}" for m in metric_order if not m.startswith("Lift")}
fmt.update({m: "{:.2f}×" for m in metric_order if m.startswith("Lift")})
st.dataframe(table.style.apply(_highlight_best, axis=0).format(fmt),
             use_container_width=True)

# Visual comparisons
st.subheader("Visual comparison")
tab1, tab2 = st.tabs(["Core metrics", "Top-k lead metrics"])

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
    st.caption("Precision@Top k% = share of real converters among the highest-"
               "scoring k% of customers — what your sales team actually calls.")

st.success(f"Evaluation complete. Best model: **{best}**. "
           "Proceed to **Lead Scoring**.")
