# © 2025 Geddy Wendot / Trivium Technology Group. All rights reserved.
# Unauthorized use, reproduction, or modification is strictly prohibited.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import joblib
import numpy as np

from src.data_cleaning import clean_data

st.set_page_config(page_title="🌾 MavunoWatch", layout="centered")

st.title("🌾 MavunoWatch - Kenyan Crop Yield Intelligence System")
st.markdown("Powered by AI. Built by G-Vector.")

# --- File Upload ---
st.header("📂 Upload CSV Data")
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    try:
        df = clean_data(uploaded_file)
        st.success("✅ Data cleaned successfully!")
        st.dataframe(df.head())

        # --- Load Model ---
        if os.path.exists("models/trained_model.pkl"):
            model = joblib.load("models/trained_model.pkl")
            st.success("✅ AI model loaded and ready.")

            # --- Filters for user input ---
            st.header("🔎 Make a Prediction")
            crop = st.selectbox("Crop Type", df["crop"].unique())
            county = st.selectbox("County", df["county"].unique())
            year = st.slider("Year", int(df["year"].min()), int(df["year"].max()), step=1)

            # Filter data based on inputs
            filtered = df[
                (df["crop"] == crop) &
                (df["county"] == county) &
                (df["year"] == year)
            ]

            if filtered.empty:
                st.warning("⚠️ No data for that combo. Try another crop/county/year.")
                st.write("🧠 Available options for your selected year:")
                st.dataframe(df[df["year"] == year][["county", "crop"]].drop_duplicates())
            else:
                row = filtered.iloc[0]
                user_input = pd.DataFrame({
                    "year": [row["year"]],
                    "rainfall_mm": [row["rainfall_mm"]],
                    "area_ha": [row["area_ha"]],
                })

                # One-hot encode crop
                for c in df["crop"].unique():
                    user_input[f"crop_{c}"] = 1 if c == crop else 0

                # Align to model features
                for col in model.feature_names_in_:
                    if col not in user_input.columns:
                        user_input[col] = 0
                user_input = user_input[model.feature_names_in_]

                prediction = model.predict(user_input)[0]
                st.subheader(f"📈 Predicted Yield: `{prediction:.2f} tons per hectare`")

        else:
            st.error("⚠️ Trained model not found. Run `model_training.py` first.")

    except Exception as e:
        st.error(f"❌ Failed to process file: {e}")

else:
    st.info("📁 Upload a .csv file to begin.")

