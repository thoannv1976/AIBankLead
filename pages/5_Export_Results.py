"""Page 6: Export Results - download the final ranked lead list."""

from datetime import datetime

import streamlit as st

from src import preprocessing, scoring, ui

ui.setup_page("Export Results", icon="📥")
ui.hero("Export Results", "Download the scored lead list for your CRM or "
        "campaign tooling.")

ui.require_models()
if st.session_state.get("lead_df") is None:
    st.info("Open **Lead Scoring** first to generate the lead table.")
    st.stop()

lead_df = st.session_state.lead_df
selected = st.session_state.get("selected_leads", lead_df)

st.subheader("What to export")
scope = st.radio("Lead scope", ["Selected top leads", "All scored customers"],
                 horizontal=True)
source = selected if scope == "Selected top leads" else lead_df

export_df = scoring.export_frame(source)

st.caption(f"Exporting **{len(export_df):,}** rows using model "
           f"**{st.session_state.get('active_model', '')}**.")
st.dataframe(export_df.head(20), use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------------
# Download buttons
# ---------------------------------------------------------------------------
stamp = datetime.now().strftime("%Y%m%d_%H%M")
csv_bytes = export_df.to_csv(index=False).encode("utf-8")
xlsx_bytes = preprocessing.to_excel_bytes(export_df, sheet_name="Leads")

d1, d2 = st.columns(2)
with d1:
    st.download_button(
        "⬇️ Download CSV", data=csv_bytes,
        file_name=f"banklead_leads_{stamp}.csv", mime="text/csv",
        use_container_width=True)
with d2:
    st.download_button(
        "⬇️ Download Excel", data=xlsx_bytes,
        file_name=f"banklead_leads_{stamp}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True)

st.divider()
st.markdown(
    "**Exported columns:** Customer ID · Rank · Lead Score · Priority · "
    "key customer features · Recommended Action."
)
st.success("Ready to download. Hand the list to your sales/CRM team and track "
           "conversions to retrain the model later.")
