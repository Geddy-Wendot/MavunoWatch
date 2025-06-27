import pandas as pd
import numpy as np

def clean_data(file_path_or_buffer):
    df = pd.read_csv(file_path_or_buffer)

    # Keep only Kenya
    if "country" in df.columns:
        df = df[df["country"].str.lower() == "kenya"]

    # Normalize columns
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={
        "admin_1": "county",
        "product": "crop",
        "harvest_year": "year",
        "area": "area_ha",
        "production": "production_tons"
    })

    # Filter by year
    df = df[pd.to_numeric(df["year"], errors="coerce") >= 2000]

    # Clean junk
    junk = ["none","n/a","nan","null","", " ", "-", "—", "all (ps)"]
    df = df.replace(junk, np.nan).infer_objects()

    # Drop rows missing critical fields
    df.dropna(subset=["year","area_ha","production_tons","crop","county"], inplace=True)

    # Convert types
    df["year"] = pd.to_numeric(df["year"])
    df["area_ha"] = pd.to_numeric(df["area_ha"])
    df["production_tons"] = pd.to_numeric(df["production_tons"])

    # Remove zero‐area rows
    df = df[df["area_ha"] > 0]

    # Compute yield
    df["yield_ton_per_ha"] = df["production_tons"] / df["area_ha"]

    if df.empty:
        raise ValueError("No data left after cleaning.")

    return df