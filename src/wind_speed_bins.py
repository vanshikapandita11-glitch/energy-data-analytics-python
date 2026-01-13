import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load 2018–19 data (skip metadata lines)
df = pd.read_csv(
    "../data/wind_data_2018_19.txt",
    sep=None,
    engine="python",
    encoding="latin1",
    skiprows=15
)

# Drop empty columns if any
df = df.dropna(axis=1, how="all")

print("Columns:", df.columns.tolist())

# Use 80m wind speed
wind_speed = df["80m Avg [m/s]"].dropna()

# Create bins (4.75–5.75 etc)
bins = np.arange(0.75, 25.75, 1)

hist, bin_edges = np.histogram(wind_speed, bins=bins)
frequency = hist / hist.sum() * 100

bin_labels = [
    f"{round(bin_edges[i],2)} - {round(bin_edges[i+1],2)}"
    for i in range(len(hist))
]

freq_df = pd.DataFrame({
    "Wind Speed Bin (m/s)": bin_labels,
    "Frequency (%)": frequency
})

print(freq_df)

# Plot
plt.figure(figsize=(10,5))
plt.bar(bin_labels, frequency)
plt.xticks(rotation=90)
plt.title("Wind Speed Frequency Distribution at 80m (2018–19)")
plt.xlabel("Wind Speed Bin (m/s)")
plt.ylabel("Frequency (%)")
plt.tight_layout()
plt.savefig("../plots/wind_speed_frequency_80m_2018_19.png")
plt.show()
