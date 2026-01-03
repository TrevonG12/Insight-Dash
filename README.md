# Insight Dash

InsightDash is an interactive data analytics dashboard built with Python, Streamlit, pandas, and Plotly.  
It loads and cleans structured sales data, computes KPI metrics, and presents interactive visualizations with filtering by date, region, category, and channel.  
A dedicated Data Quality page validates assumptions such as missing values, duplicates, and business rule consistency.

## Features
- Interactive filters (date range, region, category, channel, search)
- KPI metrics (revenue, orders, AOV, units, refund rate)
- Visualizations (time trends, category breakdown, top products)
- Data Quality checks (missing values, duplicates, type/range validation)

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run Home.py
