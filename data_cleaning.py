"""
data_cleaning.py
-----------------
Cleans the raw Supermarket Sales dataset and outputs an analysis-ready CSV.

Usage:
    python data_cleaning.py
"""

import pandas as pd
import numpy as np
import os

RAW_PATH = os.path.join("data", "supermarket_sales.csv")
CLEAN_PATH = os.path.join("data", "supermarket_sales_cleaned.csv")


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Loaded raw data: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("%", "pct")
    )
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = df.shape[0]
    df = df.drop_duplicates()
    print(f"Removed {before - df.shape[0]} duplicate rows")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    missing = df.isnull().sum()
    print("Missing values per column:\n", missing[missing > 0])

    # Numeric columns -> fill with median
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].median())

    # Categorical columns -> fill with mode
    cat_cols = df.select_dtypes(include=["object"]).columns
    for col in cat_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].mode()[0])

    # Drop rows still missing critical identifiers (e.g. invoice id)
    if "invoice_id" in df.columns:
        df = df.dropna(subset=["invoice_id"])

    return df


def fix_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    # Combine date + time into a single datetime column
    if "date" in df.columns and "time" in df.columns:
        df["datetime"] = pd.to_datetime(
            df["date"].astype(str) + " " + df["time"].astype(str),
            errors="coerce",
        )
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Numeric columns that should be float
    numeric_cols = [
        "unit_price", "quantity", "tax_5pct", "total",
        "cogs", "gross_margin_percentage", "gross_income", "rating",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Categorical columns
    cat_cols = ["branch", "city", "customer_type", "gender", "product_line", "payment"]
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].astype("category")

    return df


def remove_unnecessary_columns(df: pd.DataFrame) -> pd.DataFrame:
    # 'gross_margin_percentage' is constant (4.76% for every row) -> no analytical value
    cols_to_drop = [c for c in ["gross_margin_percentage"] if c in df.columns]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
        print(f"Dropped constant/unnecessary columns: {cols_to_drop}")
    return df


def remove_outliers_iqr(df: pd.DataFrame, cols) -> pd.DataFrame:
    before = df.shape[0]
    for col in cols:
        if col not in df.columns:
            continue
        q1, q3 = df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        df = df[(df[col] >= lower) & (df[col] <= upper)]
    print(f"Removed {before - df.shape[0]} outlier rows from {cols}")
    return df


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    if "datetime" in df.columns:
        df["hour"] = df["datetime"].dt.hour
        df["day_of_week"] = df["datetime"].dt.day_name()
        df["month"] = df["datetime"].dt.month_name()
        df["is_weekend"] = df["datetime"].dt.dayofweek.isin([5, 6])
    return df


def clean_pipeline(raw_path: str = RAW_PATH, save_path: str = CLEAN_PATH) -> pd.DataFrame:
    df = load_data(raw_path)
    df = standardize_column_names(df)
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = fix_dtypes(df)
    df = remove_unnecessary_columns(df)
    # Outlier removal is optional and commented out by default so no genuine
    # sales are discarded — uncomment if you want a stricter cleaned dataset.
    # df = remove_outliers_iqr(df, ["unit_price", "total", "quantity"])
    df = feature_engineering(df)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"\nSaved cleaned data to '{save_path}' -> {df.shape[0]} rows, {df.shape[1]} columns")
    return df


if __name__ == "__main__":
    clean_pipeline()
