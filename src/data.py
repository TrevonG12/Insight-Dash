from pathlib import Path
import pandas as pd
from scripts.generate_sample_data import generate_sample_sales_csv

DATA_PATH = Path("data") / "sample_sales.csv"

def ensure_sample_dataset():
    Path("data").mkdir(exist_ok=True)
    if not DATA_PATH.exists():
        generate_sample_sales_csv(DATA_PATH)

def load_data():
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df
