import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json

@st.cache_data
def load_data():
    df = pd.read_csv("data/kenya_only.csv")
    return df

df = load_data()
df.columns = df.columns.str.strip().str.lower()  # Normalize column names
df = df.rename(columns={"product": "crop", "admin_1": "county", "yield": "yield_ton_per_ha"})

st.set_page_config(layout="wide")
st.title("🗺️ Kenyan Crop Yield Heatmap")
st.markdown("Visualize average crop yields by county. Use the filter to view a specific crop.")

# Crop filter
all_crops = sorted(df["crop"].dropna().unique())
selected_crop = st.selectbox("Select a crop to view:", all_crops)

# Filter and group
filtered_df = df[df["crop"] == selected_crop]
grouped_df = filtered_df.groupby("county")["yield_ton_per_ha"].mean().reset_index()
grouped_df.columns = ["county", "yield"]  # Rename for clarity
grouped_df["county"] = grouped_df["county"].str.strip().str.title()  # Normalize

# Load GeoJSON
with open("data/kenya-counties-simplified.geojson", "r", encoding="utf-8") as f:
    kenya_geojson = json.load(f)

# Create Map
m = folium.Map(location=[0.0236, 37.9062], zoom_start=6)

# Choropleth
folium.Choropleth(
    geo_data=kenya_geojson,
    data=grouped_df,
    columns=["county", "yield"],
    key_on="feature.properties.shapeName",  # This is the key you confirmed exists
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=f"{selected_crop} Yield (tons/ha)",
    highlight=True
).add_to(m)

st_folium(m, width=1000, height=600)
