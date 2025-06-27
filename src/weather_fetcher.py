import requests
import pandas as pd

def fetch_power(lat, lon, start="20000101", end="20241231"):
    url = (
        f"https://power.larc.nasa.gov/api/temporal/monthly/point"
        f"?parameters=T2M,PRECTOT&community=AG&latitude={lat}&longitude={lon}"
        f"&start={start}&end={end}&format=JSON"
    )
    r = requests.get(url)
    data = r.json()["properties"]["parameter"]

    df = pd.DataFrame(data)
    df = df.T.reset_index()
    df.columns = ["year_month", "T2M", "PRECTOT"]
    df["year"] = df["year_month"].str[:4].astype(int)
    df = df.groupby("year")[["T2M", "PRECTOT"]].mean().reset_index()
    return df
