# © 2025 Geddy Wendot / Trivium Technology Group. All rights reserved.
# Unauthorized use, reproduction, or modification is strictly prohibited.

import pandas as pd
import numpy as np

def clean_data(file_path_or_buffer):
    df = pd.read_csv(file_path_or_buffer)

    # 🧠 Show what countries are present
    if "country" in df.columns:
        print("🧠 Available countries:", df["country"].unique())
        df = df[df["country"].str.lower() == "kenya"]

    # 🧽 Clean up column names
    df.columns = df.columns.str.strip().str.lower()

    # 🧱 Rename for consistency
    df = df.rename(columns={
        "admin_1": "county",
        "product": "crop",
        "harvest_year": "year",
        "area": "area_ha",
        "production": "production_tons"
    })

    # 🚫 Replace junk values with NaN
    df = df.replace(
        ["none", "None", "N/A", "n/a", "NaN", "null", "", " ", "All (PS)", "TBD", "x", "-", "—"],
        np.nan
    ).infer_objects(copy=False)

    # 🩺 Keep only valid rows
    critical_cols = ["year", "area_ha", "production_tons", "crop"]
    df.dropna(subset=critical_cols, inplace=True)

    # 🔢 Convert numerics
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["area_ha"] = pd.to_numeric(df["area_ha"], errors="coerce")
    df["production_tons"] = pd.to_numeric(df["production_tons"], errors="coerce")

    # 🚧 Drop any remaining invalid rows
    df.dropna(subset=["year", "area_ha", "production_tons"], inplace=True)

    # 🚫 Remove rows with area = 0 to prevent division errors
    df = df[df["area_ha"] > 0]

    # 📐 Feature engineering
    df["yield_ton_per_ha"] = df["production_tons"] / df["area_ha"]

    # ✅ Final sanity check
    if df.empty:
        raise ValueError("❌ No data available after cleaning. Check for invalid values in dataset.")

    return df
