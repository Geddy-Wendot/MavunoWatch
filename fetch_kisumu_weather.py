import requests
import json
import pandas as pd

# Coordinates for Kisumu, Kenya
lat, lon = -0.0917, 34.768

# Define year range
start = 2000
end = 2023

# NASA POWER API endpoint
url = (
    f"https://power.larc.nasa.gov/api/temporal/monthly/point"
    f"?parameters=T2M,PRECTOT"
    f"&community=AG"
    f"&latitude={lat}&longitude={lon}"
    f"&start={start}&end={end}"
    f"&format=JSON"
)

print("🧪 FETCH URL:", url)

# Make request
r = requests.get(url)
print("📶 Status code:", r.status_code)

if r.status_code == 200:
    try:
        data = r.json()["properties"]["parameter"]
        print("✅ Monthly weather variables:", list(data.keys()))

        # Sample value to prove structure
        jan_key = f"{start}01"
        print("🌧️ Jan precipitation sample:", data["PRECTOTCORR"][jan_key])
        print("🌡️ Jan temperature sample:", data["T2M"][jan_key])

        # Collect all records into a list of dicts
        records = []
        for year in range(start, end + 1):
            for month in range(1, 13):
                ym_key = f"{year}{month:02d}"
                try:
                    records.append({
                        "year": year,
                        "month": month,
                        "precip_mm": data["PRECTOTCORR"].get(ym_key, None),
                        "temp_C": data["T2M"].get(ym_key, None)
                    })
                except KeyError:
                    print(f"⚠️ No data for {ym_key}")

        # Convert to DataFrame
        df_weather = pd.DataFrame(records)
        print("✅ Weather data preview:")
        print(df_weather.head())

        # Save to CSV
        df_weather.to_csv("data/kisumu_weather_2000_2023.csv", index=False)
        print("💾 Saved to: data/kisumu_weather_2000_2023.csv")

    except Exception as e:
        print("❌ Unexpected format, here’s what we got:")
        print(r.json())
        print("⚠️ Error:", e)
else:
    print("❌ Weather fetch failed.")
