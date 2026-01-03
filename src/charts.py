from __future__ import annotations
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
