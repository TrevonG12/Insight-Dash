from __future__ import annotations
import pandas as pd
import numpy as np

def kpis_from_df(df: pd.DataFrame) -> dict:
    revenue = float(df["revenue"].sum())
    orders = int(df["order_id"].nunique())
    units = int(df["units"].sum())
    aov = (revenue / orders) if orders else 0.0

    # Fun portfolio metric: % of orders with >= 2 units
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

def insights_from_df(df: pd.DataFrame) -> dict:
    # Top movers: products with highest revenue
    top_movers = (
        df.groupby(["product", "category"])["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(12)
        .reset_index()
    )

    category_summary = (
        df.groupby("category")
        .agg(
            revenue=("revenue", "sum"),
            orders=("order_id", "nunique"),
            units=("units", "sum"),
            refund_rate=("refunded", "mean"),
        )
        .reset_index()
    )
    category_summary["refund_rate"] = (category_summary["refund_rate"] * 100).round(2)
    category_summary["revenue"] = category_summary["revenue"].round(2)

    return {
        "top_movers": top_movers,
        "category_summary": category_summary.sort_values("revenue", ascending=False),
    }

def data_quality_report(df: pd.DataFrame) -> dict:
    missing_by_col = df.isna().sum().sort_values(ascending=False).to_frame("missing")
    dtypes = df.dtypes.astype(str).to_frame("dtype")

    checks = []
    checks.append(("units >= 0", int((df["units"] < 0).sum())))
    checks.append(("unit_price >= 0", int((df["unit_price"] < 0).sum())))
    checks.append(("revenue >= 0", int((df["revenue"] < 0).sum())))

    # Revenue should roughly match units * unit_price
    approx = df["units"] * df["unit_price"]
    mismatch = int((np.abs(df["revenue"] - approx) > 0.01).sum())
    checks.append(("revenue == units*unit_price", mismatch))

    range_checks = pd.DataFrame(checks, columns=["check", "violations"])
    duplicate_rows = int(df.duplicated().sum())

    return {
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "duplicate_rows": duplicate_rows,
        "missing_by_col": missing_by_col,
        "dtypes": dtypes,
        "range_checks": range_checks,
    }
