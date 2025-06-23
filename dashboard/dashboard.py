# © 2025 Geddy Wendot / Trivium Technology Group. All rights reserved.
# Unauthorized use, reproduction, or modification is strictly prohibited.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from src.data_cleaning import clean_data

st.set_page_config(page_title="🌾 MavunoWatch", layout="centered")
st.title("🌾 MavunoWatch - Kenyan Crop Yield Intelligence System")
st.markdown("Built by G-Vector | Powered by Trivium Technology Group")

# --- Upload File ---
st.header("📂 Upload CSV Data")
uploaded_file = st.file_uploader("Upload your Kenya-only dataset", type=["csv"])

if uploaded_file:
    try:
        df = clean_data(uploaded_file)
        st.success(f"✅ Data cleaned successfully! Kenya-only records: {len(df)}")

        # Select County
        st.subheader("🌍 Filter by County")
        county = st.selectbox("Select County", sorted(df["county"].unique()))
        filtered_df = df[df["county"] == county]

        # Crop dropdown updates based on selected county
        crops_in_county = filtered_df["crop"].unique()
        crop = st.selectbox("Crop Type", sorted(crops_in_county))

        st.dataframe(filtered_df[filtered_df["crop"] == crop])

        # Load trained model
        if os.path.exists("models/trained_model.pkl"):
            model = joblib.load("models/trained_model.pkl")
            st.success("✅ AI model loaded and ready")

            st.header("🧮 Make a Prediction")
            year = st.slider("Year", int(df["year"].min()), int(df["year"].max()))
            area_ha = st.number_input("Land Area (Ha)", min_value=1.0, value=10.0, step=1.0)

            # Build input row for prediction
            input_data = {
                "year": year,
                "area_ha": area_ha
            }

            # Dynamic encoding for crop
            for c in df["crop"].unique():
                input_data[f"crop_{c}"] = 1 if c == crop else 0

            # Dynamic encoding for crop_production_system
            if "crop_production_system" in df.columns:
                selected_system = st.selectbox("Production System", df["crop_production_system"].dropna().unique())
                for system in df["crop_production_system"].dropna().unique():
                    input_data[f"crop_production_system_{system}"] = 1 if system == selected_system else 0

            # Align with model
            model_features = model.feature_names_in_
            input_df = pd.DataFrame([input_data])
            input_df = input_df.reindex(columns=model_features, fill_value=0)

            prediction = model.predict(input_df)[0]
            st.success(f"🌽 Estimated Yield: **{round(prediction, 2)} tons/ha**")

            # Graph actual vs predicted
            st.subheader("📊 Model Performance (All Data)")
            df_encoded = pd.get_dummies(df, columns=["crop", "crop_production_system"], drop_first=True)
            X_all = df_encoded[model_features]
            y_all = df_encoded["yield_ton_per_ha"]
            y_pred_all = model.predict(X_all)

            fig, ax = plt.subplots()
            ax.scatter(y_all, y_pred_all, alpha=0.7, color="green")
            ax.plot([y_all.min(), y_all.max()], [y_all.min(), y_all.max()], 'r--')
            ax.set_xlabel("Actual Yield (tons/ha)")
            ax.set_ylabel("Predicted Yield (tons/ha)")
            ax.set_title("Actual vs. Predicted Yield")
            st.pyplot(fig)

        else:
            st.error("⚠️ Trained model not found. Please run `model_training.py` first.")

    except Exception as e:
        st.error(f"❌ Failed to process file: {e}")
else:
    st.info("📤 Upload your Kenya-only CSV file to begin.")
