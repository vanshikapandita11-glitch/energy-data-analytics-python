import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv(
    "../data/wind_data_2017_18.txt",
    sep=None,
    engine="python",
    encoding="latin1"
)

df = df.drop(columns=["Unnamed: 17"], errors="ignore")

# Use 80 m wind data
data = df[["80m Avg [m/s]", "80m Std [m/s]"]].dropna()
data.columns = ["WindSpeed", "StdDev"]

# Turbulence Intensity
data["Turbulence"] = data["StdDev"] / data["WindSpeed"]

# Wind speed bins (0.5 m/s, centre-based)
bin_edges = np.arange(0.25, data["WindSpeed"].max() + 0.75, 0.5)

data["Speed_Bin"] = pd.cut(
    data["WindSpeed"],
    bins=bin_edges,
    include_lowest=True
)

# Bin centre
data["Bin_Centre"] = data["Speed_Bin"].apply(
    lambda x: round((x.left + x.right) / 2, 2)
)

# Bin-wise averages
summary = (
    data
    .groupby("Bin_Centre")
    .agg(
        Mean_WindSpeed=("WindSpeed", "mean"),
        Mean_Turbulence=("Turbulence", "mean")
    )
    .reset_index()
)
print(summary)

plt.figure(figsize=(7,5))
plt.scatter(
    data["WindSpeed"],
    data["Turbulence"],
    alpha=0.3
)

plt.xlabel("Wind Speed (m/s)")
plt.ylabel("Turbulence Intensity")
plt.title("Turbulence Intensity vs Wind Speed (80 m)")
plt.grid(True)

plt.savefig("../plots/turbulence_vs_windspeed_scatter_80m.png", dpi=300)
plt.show()

plt.figure(figsize=(7,5))
plt.plot(
    summary["Mean_WindSpeed"],
    summary["Mean_Turbulence"],
    marker="o"
)

plt.xlabel("Mean Wind Speed (m/s)")
plt.ylabel("Mean Turbulence Intensity")
plt.title("Bin-wise Turbulence Intensity vs Wind Speed (80 m)")
plt.grid(True)

plt.savefig("../plots/turbulence_vs_windspeed_binwise_80m.png", dpi=300)
plt.show()
