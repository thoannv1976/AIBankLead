"""Page 6: Export Results - download the final ranked lead list."""

from datetime import datetime

import streamlit as st

from src import preprocessing, scoring, ui

ui.setup_page("Export Results", icon="📥")
ui.hero(ui.T("export.title"), ui.T("export.subtitle"))

ui.require_models()
if st.session_state.get("lead_df") is None:
    st.info(ui.T("insights.open_scoring_info"))
    st.stop()

lang = ui.get_lang()
lead_df = st.session_state.lead_df
selected = st.session_state.get("selected_leads", lead_df)

st.subheader(ui.T("export.what_to_export"))
scope_keys = ["scope.selected", "scope.all"]
scope = st.radio(ui.T("export.lead_scope"), scope_keys, horizontal=True,
                 format_func=lambda k: ui.T(k))
source = selected if scope == "scope.selected" else lead_df

# Build the canonical (English) export frame, then localize for display/output.
export_df = scoring.localize_lead_df(scoring.export_frame(source), lang)

st.caption(ui.T("export.exporting_caption", n=len(export_df),
                model=st.session_state.get("active_model", "")))
st.dataframe(export_df.head(20), use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------------
# Download buttons
# ---------------------------------------------------------------------------
stamp = datetime.now().strftime("%Y%m%d_%H%M")
csv_bytes = export_df.to_csv(index=False).encode("utf-8-sig")
xlsx_bytes = preprocessing.to_excel_bytes(export_df, sheet_name="Leads")

d1, d2 = st.columns(2)
with d1:
    st.download_button(
        ui.T("export.download_csv"), data=csv_bytes,
        file_name=f"banklead_leads_{stamp}.csv", mime="text/csv",
        use_container_width=True)
with d2:
    st.download_button(
        ui.T("export.download_excel"), data=xlsx_bytes,
        file_name=f"banklead_leads_{stamp}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True)

st.divider()
st.markdown(ui.T("export.exported_columns"))
st.success(ui.T("export.success"))
