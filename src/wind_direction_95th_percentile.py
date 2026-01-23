import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Load raw wind data
# -----------------------------
df = pd.read_csv(
    "../data/wind_data_2017_18.txt",
    sep=None,
    engine="python",
    encoding="latin1"
)

df = df.drop(columns=["Unnamed: 17"], errors="ignore")

# Select required columns
data = df[["80m Avg [m/s]", "78m WV [°]"]].dropna()
data.columns = ["speed", "direction"]

# -----------------------------
# Direction sector function
# -----------------------------
def direction_sector(angle):
    if (angle >= 337.5) or (angle < 22.5):
        return "N", 0
    elif angle < 67.5:
        return "NE", 45
    elif angle < 112.5:
        return "E", 90
    elif angle < 157.5:
        return "SE", 135
    elif angle < 202.5:
        return "S", 180
    elif angle < 247.5:
        return "SW", 225
    elif angle < 292.5:
        return "W", 270
    else:
        return "NW", 315

data[["Dir", "Angle"]] = data["direction"].apply(
    lambda x: pd.Series(direction_sector(x))
)

# -----------------------------
# 95th percentile calculation
# -----------------------------
p95_table = (
    data
    .groupby(["Dir", "Angle"])["speed"]
    .quantile(0.95)
    .reset_index(name="95th Percentile Speed (m/s)")
)

print(p95_table)

# -----------------------------
# Polar plot
# -----------------------------
theta = np.deg2rad(p95_table["Angle"])
r = p95_table["95th Percentile Speed (m/s)"]

fig = plt.figure(figsize=(7, 7))
ax = plt.subplot(111, polar=True)

ax.plot(theta, r, marker="o")
ax.fill(theta, r, alpha=0.3)

ax.set_xticks(np.deg2rad([0,45,90,135,180,225,270,315]))
ax.set_xticklabels(["N","NE","E","SE","S","SW","W","NW"])

ax.set_title(
    "95th Percentile Wind Speed by Direction (2017–18)",
    pad=20
)

plt.show()
