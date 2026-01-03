import streamlit as st
from src.data import load_data, ensure_sample_dataset
from src.ui import app_header, sidebar_filters
from src.metrics import insights_from_df
from src.charts import chart_revenue_by_category

st.set_page_config(page_title="Insights • InsightDash", layout="wide")

ensure_sample_dataset()
df = load_data()

app_header("Insights", "What’s driving revenue and where it’s coming from")

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

ins = insights_from_df(fdf)

st.subheader("Top movers (Revenue)")
st.dataframe(ins["top_movers"], use_container_width=True)

st.subheader("Category summary")
st.dataframe(ins["category_summary"], use_container_width=True)

st.divider()
st.plotly_chart(chart_revenue_by_category(fdf), use_container_width=True)
