# © 2025 Geddy Wendot / Trivium Technology Group. All rights reserved.
# Unauthorized use, reproduction, or modification is strictly prohibited.

import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from datetime import datetime
import folium
import json
from streamlit_folium import folium_static

# Fix module path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__) if "__file__" in globals() else os.getcwd())
sys.path.append(os.path.abspath(os.path.join(CURRENT_DIR, '..')))

from src.data_cleaning import clean_data

st.set_page_config(page_title="🌾 MavunoWatch", layout="wide")
st.title("🌾 MavunoWatch - Kenyan Crop Yield Intelligence System")
st.markdown("Built by G-Vector | Powered by Trivium Technology Group")

# --- Upload File ---
st.sidebar.header("📂 Upload Your Crop Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    try:
        df = clean_data(uploaded_file)
        st.success(f"✅ Data cleaned successfully. Records from Kenya: {len(df)}")
        st.dataframe(df.head(), use_container_width=True)

        if os.path.exists("models/trained_model.pkl"):
            model = joblib.load("models/trained_model.pkl")
            st.sidebar.success("✅ AI model loaded!")

            # --- Prediction ---
            st.header("🔍 Predict Crop Yield")
            county = st.selectbox("County", sorted(df["county"].unique()))
            crops = sorted(df[df["county"] == county]["crop"].unique())
            crop = st.selectbox("Crop Type", crops)
            area_ha = st.number_input("Land Area (Ha)", min_value=1.0, value=10.0)
            year = datetime.now().year

            input_data = {"year": year, "area_ha": area_ha}
            for c in df["crop"].unique():
                input_data[f"crop_{c}"] = 1 if c == crop else 0
            model_features = model.feature_names_in_
            input_df = pd.DataFrame([input_data])[model_features]
            prediction = model.predict(input_df)[0]
            st.success(f"🌽 Estimated Yield for {crop} in {county} ({year}): **{round(prediction, 2)} tons/ha**")

            # --- Best Crop ---
            st.subheader("🏆 Best-Performing Crop Recommendation")
            best_preds = []
            for c in crops:
                row = {"year": year, "area_ha": area_ha}
                for k in df["crop"].unique():
                    row[f"crop_{k}"] = 1 if k == c else 0
                try:
                    row_df = pd.DataFrame([row])[model_features]
                    yield_val = model.predict(row_df)[0]
                    best_preds.append((c, yield_val))
                except Exception:
                    continue

            if best_preds:
                sorted_df = pd.DataFrame(best_preds, columns=["Crop", "Predicted Yield"]).sort_values(by="Predicted Yield", ascending=False)
                top_crop = sorted_df.iloc[0]
                st.success(f"🥇 **Recommended Crop** for {county}: **{top_crop['Crop']}** → **{round(top_crop['Predicted Yield'], 2)} tons/ha**")
                st.bar_chart(sorted_df.set_index("Crop"))
            else:
                st.warning("⚠️ No crop predictions available.")

            # --- Yield Trend ---
            st.subheader("📈 Yield Trend Over Time")
            trend_crop = st.selectbox("Select Crop to Visualize", crops)
            trend_df = df[(df["county"] == county) & (df["crop"] == trend_crop)].groupby("year")["yield_ton_per_ha"].mean().reset_index()
            if len(trend_df) > 1:
                fig, ax = plt.subplots()
                ax.plot(trend_df["year"], trend_df["yield_ton_per_ha"], marker='o', color='green')
                ax.set_title(f"Yield Trend for {trend_crop} in {county}")
                ax.set_xlabel("Year")
                ax.set_ylabel("Yield (tons/ha)")
                st.pyplot(fig)

                slope = np.polyfit(trend_df["year"], trend_df["yield_ton_per_ha"], 1)[0]
                if slope > 0.2:
                    st.info("📈 Yield is increasing. Good investment potential.")
                elif slope < -0.2:
                    st.warning("📉 Declining yield trend. Monitor closely.")
                else:
                    st.info("⚖️ Yield is relatively stable.")
            else:
                st.warning("📎 Not enough data to show yield trend.")

            # --- Model Performance ---
            st.subheader("📊 Model Evaluation")
            df_encoded = pd.get_dummies(df, columns=["crop"], drop_first=True)
            X_all = df_encoded[model_features]
            y_all = df_encoded["yield_ton_per_ha"]
            y_pred_all = model.predict(X_all)

            fig2, ax2 = plt.subplots()
            ax2.scatter(y_all, y_pred_all, alpha=0.5, color="blue")
            ax2.plot([y_all.min(), y_all.max()], [y_all.min(), y_all.max()], 'r--')
            ax2.set_title("Model Prediction vs Actual Yield")
            ax2.set_xlabel("Actual Yield (tons/ha)")
            ax2.set_ylabel("Predicted Yield (tons/ha)")
            st.pyplot(fig2)

            # --- Heatmap ---
            st.header("🗺️ Kenya Yield Heatmap")
            selected_crop = st.selectbox("🌾 Filter by Crop", sorted(df["crop"].unique()))
            filtered_df = df[df["crop"] == selected_crop]
            avg_yield = filtered_df.groupby("county")["yield_ton_per_ha"].mean().reset_index()
            avg_yield.columns = ["county", "avg_yield"]
            avg_yield["county"] = avg_yield["county"].str.title().str.strip()

            geo_path = "data/kenya-counties-simplified.geojson"
            if os.path.exists(geo_path):
                with open(geo_path, "r", encoding="utf-8") as f:
                    geo_data = json.load(f)

                # Attach average yield to GeoJSON features
                county_yield_map = dict(zip(avg_yield["county"], avg_yield["avg_yield"]))
                for feature in geo_data["features"]:
                    county_name = feature["properties"].get("shapeName", "").title().strip()
                    feature["properties"]["avg_yield"] = round(county_yield_map.get(county_name, 0.0), 2)

                m = folium.Map(location=[0.02, 37.9], zoom_start=6)

                choropleth = folium.Choropleth(
                    geo_data=geo_data,
                    data=avg_yield,
                    columns=["county", "avg_yield"],
                    key_on="feature.properties.shapeName",
                    fill_color="YlGn",
                    fill_opacity=0.7,
                    line_opacity=0.2,
                    legend_name="Avg Yield (tons/ha)",
                    highlight=True
                )
                choropleth.add_to(m)

                folium.GeoJson(
                    geo_data,
                    style_function=lambda x: {"fillOpacity": 0},
                    tooltip=folium.GeoJsonTooltip(
                        fields=["shapeName", "avg_yield"],
                        aliases=["County", "Predicted Yield (tons/ha)"],
                        localize=True,
                        sticky=False,
                        labels=True
                    )
                ).add_to(m)

                folium_static(m, width=900, height=500)
            else:
                st.warning("GeoJSON file not found. Place it at `data/kenya-counties-simplified.geojson`.")

        else:
            st.error("⚠️ No trained model found. Run `model_training.py` first.")

    except Exception as e:
        st.error(f"❌ Failed to process file: {e}")
else:
    st.info("📎 Upload a cleaned CSV file to get started.")
