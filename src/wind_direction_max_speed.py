import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "../data/wind_data_2017_18.txt",
    sep=None,
    engine="python",
    encoding="latin1"
)

df = df.drop(columns=["Unnamed: 17"], errors="ignore")

data = df[["80m Avg [m/s]", "78m WV [°]"]].dropna()
data.columns = ["speed", "direction"]

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

# Calculate maximum wind speed for each direction
max_speed = data.groupby("Direction")["speed"].max()

# Order directions properly
order = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
max_speed = max_speed.reindex(order)

# Plot
plt.figure(figsize=(7, 4))
plt.bar(max_speed.index, max_speed.values)
plt.xlabel("Wind Direction")
plt.ylabel("Maximum Wind Speed (m/s)")
plt.title("Maximum Wind Speed by Direction (2017–18)")
plt.tight_layout()

# Save for PPT
plt.savefig(
    "../plots/max_wind_speed_by_direction_2017_18.png",
    dpi=300
)

plt.show()