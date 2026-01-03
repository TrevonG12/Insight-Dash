from __future__ import annotations
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
