import streamlit as st
from src.data import load_data, ensure_sample_dataset
from src.ui import app_header, sidebar_filters
from src.metrics import kpis_from_df
from src.charts import chart_revenue_over_time, chart_revenue_by_category, chart_top_products

st.set_page_config(page_title="Dashboard • InsightDash", layout="wide")

ensure_sample_dataset()
df = load_data()

app_header("Dashboard", "KPIs + trends with clean filtering")

filters = sidebar_filters(df)
fdf = df.copy()

if filters["date_range"]:
    start, end = filters["date_range"]
    fdf = fdf[(fdf["date"] >= start) & (fdf["date"] <= end)]

if filters["region"] != "All":
    fdf = fdf[fdf["region"] == filters["region"]]
if filters["category"] != "All":
    fdf = fdf[fdf["category"] == filters["category"]]
if filters["channel"] != "All":
    fdf = fdf[fdf["channel"] == filters["channel"]]
if filters["search"].strip():
    s = filters["search"].strip().lower()
    fdf = fdf[fdf["product"].str.lower().str.contains(s)]

k = kpis_from_df(fdf)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"${k['revenue']:,.0f}")
c2.metric("Orders", f"{k['orders']:,}")
c3.metric("Avg Order Value", f"${k['aov']:,.2f}")
c4.metric("Refund Rate", f"{k['refund_rate']:.2f}%")

st.divider()
st.plotly_chart(chart_revenue_over_time(fdf), use_container_width=True)
st.plotly_chart(chart_revenue_by_category(fdf), use_container_width=True)
st.plotly_chart(chart_top_products(fdf, top_n=10), use_container_width=True)
