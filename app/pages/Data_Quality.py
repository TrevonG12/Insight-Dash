import streamlit as st
from src.data import load_data, ensure_sample_dataset
from src.ui import app_header
from src.metrics import data_quality_report

st.set_page_config(page_title="Data Quality • InsightDash", layout="wide")

ensure_sample_dataset()
df = load_data()

app_header("Data Quality", "Missing values, duplicates, ranges, and type checks")

report = data_quality_report(df)

c1, c2, c3 = st.columns(3)
c1.metric("Rows", f"{report['rows']:,}")
c2.metric("Columns", f"{report['cols']:,}")
c3.metric("Duplicate Rows", f"{report['duplicate_rows']:,}")

st.divider()
st.subheader("Missing values by column")
st.dataframe(report["missing_by_col"], use_container_width=True)

st.subheader("Value range checks")
st.dataframe(report["range_checks"], use_container_width=True)
