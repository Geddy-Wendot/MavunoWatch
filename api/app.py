# © 2025 Geddy Wendot / Trivium Technology Group. All rights reserved.
# Unauthorized use, reproduction, or modification is strictly prohibited.

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import os
import sys

# Path setup
app = Flask(__name__)
CORS(app)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

from src.data_cleaning import clean_data

# Load model and base year
MODEL_PATH = os.path.join(BASE_DIR, "models", "trained_model.pkl")
BASE_YEAR_PATH = os.path.join(BASE_DIR, "models", "base_year.txt")
DATA_PATH = os.path.join(BASE_DIR, "data", "kenya_only.csv")

model = joblib.load(MODEL_PATH)
print("✅ Loaded model from:", MODEL_PATH)

with open(BASE_YEAR_PATH, "r") as f:
    base_year = int(f.read().strip())
print("📦 Loaded base year:", base_year)

# Load and clean the data for metadata and trends
df = clean_data(DATA_PATH)

@app.route("/")
def index():
    return jsonify({"message": "🌾 MavunoWatch API is running!"})

@app.route("/metadata", methods=["GET"])
def metadata():
    counties = sorted(df["county"].dropna().unique().tolist())
    crops = sorted(df["crop"].dropna().unique().tolist())
    return jsonify({"counties": counties, "crops": crops})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        year = int(data["year"])
        area_ha = float(data["area_ha"])
        crop = data["crop"]
        all_crops = data["all_crops"]

        # Convert year to year_since_start
        year_since_start = year - base_year

        # Build input vector
        input_data = {"year_since_start": year_since_start, "area_ha": area_ha}
        for c in all_crops:
            input_data[f"crop_{c}"] = 1 if c == crop else 0

        input_df = pd.DataFrame([input_data])[model.feature_names_in_]
        predicted_yield = model.predict(input_df)[0]

        return jsonify({
            "predicted_yield": round(predicted_yield, 2),
            "units": "tons/ha"
        })

    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 400

@app.route("/trend", methods=["POST"])
def trend():
    try:
        data = request.get_json()
        county = data["county"]
        crop = data["crop"]

        trend_df = df[(df["county"] == county) & (df["crop"] == crop)]
        if trend_df.empty:
            return jsonify({"error": "No data found for selected county and crop."})

        trend = trend_df.groupby("year")["yield_ton_per_ha"].mean().reset_index()

        slope = np.polyfit(trend["year"], trend["yield_ton_per_ha"], 1)[0]
        note = "⚖️ Yield is relatively stable."
        if slope > 0.2:
            note = "📈 Yield is increasing. Good trend."
        elif slope < -0.2:
            note = "📉 Yield is decreasing. Caution advised."

        return jsonify({
            "trend": trend.to_dict(orient="records"),
            "trend_note": note
        })

    except Exception as e:
        return jsonify({"error": f"Trend analysis failed: {str(e)}"}), 400

if __name__ == "__main__":
    app.run(debug=True)
