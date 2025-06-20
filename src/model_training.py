# © 2025 Geddy Wendot / Trivium Technology Group. All rights reserved.
# Unauthorized use, reproduction, or modification is strictly prohibited.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import joblib
from src.data_cleaning import clean_data

def train_model():
    """
    Loads and cleans the dataset, trains a RandomForestRegressor model,
    evaluates it, and saves it to disk.
    """
    # Load and clean data
    df = clean_data("data/kenya_food_production.csv")

    # One-hot encode 'crop' for model input
    df_encoded = pd.get_dummies(df, columns=['crop'], drop_first=True)

    # Define features and target
    feature_cols = ['year', 'rainfall_mm', 'area_ha'] + [col for col in df_encoded.columns if 'crop_' in col]
    X = df_encoded[feature_cols]
    y = df_encoded['yield_ton_per_ha']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    preds = model.predict(X_test)
    print("📊 Model Evaluation:")
    
    print("RMSE:", np.sqrt(mean_squared_error(y_test, preds)))

    print("MAE :", mean_absolute_error(y_test, preds))

    # Save model
    joblib.dump(model, "models/trained_model.pkl")
    print("✅ Model saved to models/trained_model.pkl")

if __name__ == "__main__":
    train_model()
