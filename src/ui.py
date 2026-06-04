"""Shared Streamlit UI helpers: theming, headers, priority badges."""

from __future__ import annotations

import streamlit as st

from . import config

CUSTOM_CSS = f"""
<style>
    .main {{ background-color: {config.COLORS['white']}; }}
    h1, h2, h3 {{ color: {config.COLORS['primary']}; }}
    .bl-hero {{
        background: linear-gradient(120deg, {config.COLORS['primary']} 0%,
                    {config.COLORS['primary_light']} 100%);
        padding: 1.4rem 1.8rem; border-radius: 14px; color: white;
        margin-bottom: 1.2rem;
    }}
    .bl-hero h1 {{ color: white !important; margin: 0; font-size: 1.9rem; }}
    .bl-hero p {{ color: #DCE6F7; margin: 0.4rem 0 0 0; font-size: 1rem; }}
    .bl-pill {{
        display: inline-block; padding: 0.15rem 0.7rem; border-radius: 999px;
        font-size: 0.8rem; font-weight: 600; color: white;
    }}
    div[data-testid="stMetric"] {{
        background: {config.COLORS['light_grey']};
        border: 1px solid #E3E8F0; border-radius: 12px;
        padding: 0.8rem 1rem;
    }}
</style>
"""


def setup_page(title: str, icon: str = "🏦"):
    """Apply page config + global CSS. Call once at the top of each page."""
    st.set_page_config(page_title=f"BankLead AI - {title}", page_icon=icon,
                       layout="wide", initial_sidebar_state="expanded")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str):
    """Render the gradient hero header."""
    st.markdown(
        f"<div class='bl-hero'><h1>{title}</h1><p>{subtitle}</p></div>",
        unsafe_allow_html=True,
    )


def priority_badge(priority: str) -> str:
    """Return an HTML pill for a priority band."""
    color = config.PRIORITY_COLORS.get(priority, config.COLORS["grey"])
    return f"<span class='bl-pill' style='background:{color}'>{priority}</span>"


def style_lead_table(df):
    """Apply background colors to the Priority column of a lead table."""
    def color_priority(val):
        color = config.PRIORITY_COLORS.get(val, "#FFFFFF")
        return f"background-color: {color}; color: white; font-weight:600;"

    styler = df.style
    if "Priority" in df.columns:
        styler = styler.map(color_priority, subset=["Priority"])
    if "Lead Score" in df.columns:
        styler = styler.format({"Lead Score": "{:.3f}"})
    return styler


def require_data():
    """Guard: stop the page if no dataset is loaded yet."""
    if "raw_df" not in st.session_state or st.session_state.raw_df is None:
        st.warning("No data loaded yet. Go to **Upload & Preview** to load a CSV "
                   "(or load the bundled sample dataset).")
        st.stop()


def require_models():
    """Guard: stop the page if models haven't been trained."""
    require_data()
    if not st.session_state.get("models"):
        st.warning("No trained models yet. Go to **Train & Evaluate** first.")
        st.stop()
