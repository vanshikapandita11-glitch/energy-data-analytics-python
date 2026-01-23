import pandas as pd
import numpy as np

# LOAD 2018-18 WIND DATA

df = pd.read_csv(
    "../data/wind_data_2017_18.txt",
    sep=None,
    engine="python",
    encoding="latin1"
)

df = df.drop(columns=["Unnamed: 17"], errors="ignore")

wind_speed = df["80m Avg [m/s]"].dropna()

#Bin settings

bin_width = 0.5
total_hours_year = len(wind_speed) / 6

min_speed = 0
max_speed = np.ceil(wind_speed.max())

bin_edges = np.arange(min_speed, max_speed + bin_width, bin_width)
bin_centres = bin_edges[:-1] + bin_width / 2

results = []

for low, high, centre in zip(bin_edges[:-1], bin_edges[1:], bin_centres):
    count = ((wind_speed >= low) & (wind_speed < high)).sum()
    hours = count/6
    frequency = (hours / total_hours_year) * 100

    results.append([centre, low, high, count, hours, frequency])

freq_df = pd.DataFrame(
    results,
    columns=[
        "Bin Centre (m/s)",
        "Lower Bound (m/s)",
        "Upper Bound (m/s)",
        "Data Points",
        "Hours per Year",
        "Frequency (%)"
    ]
)

print(freq_df)

print("\nCHECKS")
print("Total hours:", freq_df["Hours per Year"].sum())
print("Total Frequency (%):", freq_df["Frequency (%)"].sum())
