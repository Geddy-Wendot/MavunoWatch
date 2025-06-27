import pandas as pd

# Load yield data
yield_df = pd.read_csv("data/kenya_only.csv")
yield_df = yield_df[yield_df["county"].str.lower() == "kisumu"]
yield_df = yield_df[yield_df["harvest_year"] >= 2000]
yield_df = yield_df.dropna(subset=["yield"])

# Create month column (if not available, you can assume harvest happens in a specific month, like October)
yield_df["month"] = 10  # Or adjust based on your logic

# Load weather data
weather_df = pd.read_csv("data/kisumu_weather_2000_2023.csv")

# Merge on year and month
merged_df = pd.merge(
    yield_df,
    weather_df,
    left_on=["harvest_year", "month"],
    right_on=["year", "month"],
    how="left"
)

# Drop duplicate year col
merged_df.drop(columns=["year"], inplace=True)

# Save the merged dataset
merged_df.to_csv("data/yield_with_weather.csv", index=False)
print("✅ Merged data saved to: data/yield_with_weather.csv")
