import pandas as pd
df = pd.read_csv("data/kenya_only.csv")
df["product"] = df["product"].str.strip().str.lower()
df[df["product"] == "maize"]

import pandas as pd

df = pd.read_csv("data/kenya_only.csv")
df = df[df["product"].str.lower() == "maize"]
df = df[df["harvest_year"] >= 1990]
df = df.dropna(subset=["yield"])

print("Years in data:", df["harvest_year"].unique())
print("Yield stats by year:")
print(df.groupby("harvest_year")["yield"].describe())
print("Correlation between year and yield:", df[["harvest_year", "yield"]].corr())