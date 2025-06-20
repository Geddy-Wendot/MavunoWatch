# © 2025 Geddy Wendot / Trivium Technology Group. All rights reserved.
# Unauthorized use, reproduction, or modification is strictly prohibited.

import pandas as pd

def clean_data(filepath):
    """
    Loads, cleans, and engineers features from the food production dataset.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Cleaned and feature-engineered dataframe.
    """
    # Load data
    df = pd.read_csv(filepath)

    # Normalize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Drop rows with missing values (can later be replaced with smarter imputation)
    df.dropna(inplace=True)

    # Feature engineering: yield per hectare
    df['yield_ton_per_ha'] = df['production_tons'] / df['area_ha']

    return df
