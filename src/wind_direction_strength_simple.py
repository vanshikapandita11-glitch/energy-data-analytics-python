import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv(
    "../data/wind_data_2017_18.txt",
    sep=None,
    engine="python",
    encoding="latin1"
)

df = df.drop(columns=["Unnamed: 17"], errors="ignore")

data = df[["80m Avg [m/s]", "78m WV [°]"]].dropna()
data.columns = ["speed", "direction"]

# Direction classification
def direction_sector(angle):
    if (angle >= 337.5) or (angle < 22.5):
        return "N"
    elif angle < 67.5:
        return "NE"
    elif angle < 112.5:
        return "E"
    elif angle < 157.5:
        return "SE"
    elif angle < 202.5:
        return "S"
    elif angle < 247.5:
        return "SW"
    elif angle < 292.5:
        return "W"
    else:
        return "NW"

data["Direction"] = data["direction"].apply(direction_sector)

# 95th percentile wind speed per direction
p95 = data.groupby("Direction")["speed"].quantile(0.95)

# Order directions nicely
order = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
p95 = p95.reindex(order)

# Plot
plt.figure(figsize=(8, 5))
plt.bar(p95.index, p95.values)

plt.xlabel("Wind Direction")
plt.ylabel("Wind Speed (m/s)")
plt.title("Directional Extreme Wind Strength (2017–18)")

plt.tight_layout()
plt.savefig(
    "../plots/directional_95th_percentile_wind_speed_2017_18.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
