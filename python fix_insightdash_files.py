from pathlib import Path

ROOT = Path(".").resolve()

def write(path: str, content: str):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print("Wrote:", path)

FILES = {
"src/__init__.py": "# package marker\n",

"src/ui.py": """from __future__ import annotations
import streamlit as st
import pandas as pd

def app_header(title: str, subtitle: str):
    st.markdown(
        f\"\"\"
        <div style="padding: 0.2rem 0 1.0rem 0;">
          <h1 style="margin-bottom:0.15rem;">{title}</h1>
          <p style="margin-top:0;color:#9CA3AF;font-size:1.05rem;">{subtitle}</p>
        </div>
        \"\"\",
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
""",

"src/metrics.py": """from __future__ import annotations
import pandas as pd
import numpy as np

def kpis_from_df(df: pd.DataFrame) -> dict:
    revenue = float(df["revenue"].sum())
    orders = int(df["order_id"].nunique())
    units = int(df["units"].sum())
    aov = (revenue / orders) if orders else 0.0

    if orders:
        orders_units = df.groupby("order_id")["units"].sum()
        conversion_proxy = float((orders_units.ge(2).mean()) * 100)
    else:
        conversion_proxy = 0.0

    refund_rate = float(df["refunded"].mean() * 100) if len(df) else 0.0

    return {
        "revenue": revenue,
        "orders": orders,
        "units": units,
        "aov": aov,
        "conversion_proxy": conversion_proxy,
        "refund_rate": refund_rate,
    }
""",

"src/charts.py": """from __future__ import annotations
import pandas as pd
import plotly.express as px

def chart_revenue_over_time(df: pd.DataFrame):
    g = df.groupby("date", as_index=False)["revenue"].sum()
    fig = px.line(g, x="date", y="revenue", markers=True, title="Revenue Over Time")
    fig.update_layout(margin=dict(l=10, r=10, t=60, b=10))
    return fig

def chart_revenue_by_category(df: pd.DataFrame):
    g = df.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    fig = px.bar(g, x="category", y="revenue", title="Revenue by Category")
    fig.update_layout(margin=dict(l=10, r=10, t=60, b=10))
    return fig

def chart_top_products(df: pd.DataFrame, top_n: int = 10):
    g = (
        df.groupby("product", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .head(top_n)
    )
    fig = px.bar(g, x="revenue", y="product", orientation="h", title=f"Top {top_n} Products by Revenue")
    fig.update_layout(margin=dict(l=10, r=10, t=60, b=10), yaxis=dict(autorange="reversed"))
    return fig
""",

"scripts/generate_sample_data.py": """from __future__ import annotations
from pathlib import Path
import random
from datetime import date, timedelta
import csv

REGIONS = ["Midwest", "South", "Northeast", "West"]
CHANNELS = ["Online", "In-Store", "Wholesale"]
CATEGORIES = ["Outdoor", "Home", "Fitness", "Electronics", "Fashion"]

PRODUCTS = {
    "Outdoor": ["Trail Backpack", "Camping Lantern", "Water Bottle", "Hiking Poles", "Tent Repair Kit"],
    "Home": ["LED Bulbs", "Smart Plug", "Vacuum Filters", "Kitchen Scale", "Air Purifier Filter"],
    "Fitness": ["Resistance Bands", "Foam Roller", "Protein Shaker", "Yoga Mat", "Jump Rope"],
    "Electronics": ["USB-C Hub", "Wireless Charger", "Bluetooth Speaker", "Keyboard", "Webcam"],
    "Fashion": ["Beanie", "Hoodie", "Socks Pack", "Cap", "Windbreaker"],
}

def generate_sample_sales_csv(out_path: Path, days: int = 180, rows_per_day: int = 35) -> None:
    random.seed(42)
    start = date.today() - timedelta(days=days)

    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date","order_id","region","channel","category","product","units","unit_price","revenue","refunded"])

        order_counter = 100000
        for d in range(days):
            day = start + timedelta(days=d)

            for _ in range(rows_per_day):
                order_counter += 1
                region = random.choice(REGIONS)
                channel = random.choice(CHANNELS)
                category = random.choice(CATEGORIES)
                product = random.choice(PRODUCTS[category])

                units = random.randint(1, 5)
                base = {"Outdoor": 28, "Home": 22, "Fitness": 25, "Electronics": 45, "Fashion": 30}[category]
                unit_price = round(random.uniform(base * 0.8, base * 1.35), 2)

                season_boost = 1.0 + (0.12 if (day.month in [11, 12]) else 0.0)
                region_boost = {"West": 1.04, "South": 1.02, "Midwest": 0.98, "Northeast": 1.00}[region]
                revenue = round(units * unit_price * season_boost * region_boost, 2)

                refunded = random.random() < 0.03
                w.writerow([day.isoformat(), f"ORD-{order_counter}", region, channel, category, product, units, unit_price, revenue, refunded])
""",
}

def main():
    for p, c in FILES.items():
        write(p, c)

    # Ensure data folder exists; CSV will be created by ensure_sample_dataset()
    (ROOT / "data").mkdir(parents=True, exist_ok=True)

    print("\\n✅ Missing files created. Now run:")
    print("   streamlit run app/Home.py")

if __name__ == "__main__":
    main()
