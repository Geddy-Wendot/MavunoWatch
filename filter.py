import pandas as pd

df = pd.read_csv("data/hvstat_africa_data_v1.0.csv")
kenya_df = df[df["country"] == "Kenya"]

# Save filtered Kenya data
kenya_df.to_csv("data/kenya_real.csv", index=False)
