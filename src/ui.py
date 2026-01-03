from __future__ import annotations
import streamlit as st
import pandas as pd

def app_header(title: str, subtitle: str):
    st.markdown(
        f"""
        <div style="padding: 0.2rem 0 1.0rem 0;">
          <h1 style="margin-bottom:0.15rem;">{title}</h1>
          <p style="margin-top:0;color:#9CA3AF;font-size:1.05rem;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def sidebar_filters(df: pd.DataFrame) -> dict:
    st.sidebar.header("Filters")

    min_d = df["date"].min()
    max_d = df["date"].max()
    date_range = st.sidebar.date_input("Date range", value=(min_d, max_d))

    dr = date_range if isinstance(date_range, tuple) and len(date_range) == 2 else None

    regions = ["All"] + sorted(df["region"].unique().tolist())
    categories = ["All"] + sorted(df["category"].unique().tolist())
    channels = ["All"] + sorted(df["channel"].unique().tolist())

    region = st.sidebar.selectbox("Region", regions, index=0)
    category = st.sidebar.selectbox("Category", categories, index=0)
    channel = st.sidebar.selectbox("Channel", channels, index=0)
    search = st.sidebar.text_input("Search product", value="")

    st.sidebar.markdown("---")
    st.sidebar.caption("Tip: Try filtering Category + Region to see shifts.")

    return {
        "date_range": dr,
        "region": region,
        "category": category,
        "channel": channel,
        "search": search,
    }
