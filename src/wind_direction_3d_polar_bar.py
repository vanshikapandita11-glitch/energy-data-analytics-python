import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# -----------------------------
# Load precomputed table
# -----------------------------
df = pd.read_csv(
    "../data/wind_direction_speed_table_2017_18.csv"
)

# Keep only non-zero frequency for plotting
df = df[df["Frequency (%)"] > 0]

# -----------------------------
# Extract bin centres from Speed_Bin
# -----------------------------
def bin_center(bin_str):
    low, high = bin_str.strip("[]()").split(",")
    return (float(low) + float(high)) / 2

df["Speed_Center"] = df["Speed_Bin"].astype(str).apply(bin_center)

# -----------------------------
# Convert to polar coordinates
# -----------------------------
theta = np.deg2rad(df["Angle"].values)   # angle
r = df["Speed_Center"].values             # radius
z = np.zeros(len(df))                     # base
dz = df["Frequency (%)"].values           # bar height

# Bar width settings
dtheta = np.deg2rad(360 / 8) * 0.8
dr = 0.4

# -----------------------------
# Plot
# -----------------------------
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

ax.bar3d(theta, r, z, dtheta, dr, dz)

ax.set_xlabel("Wind Direction (rad)")
ax.set_ylabel("Wind Speed (m/s)")
ax.set_zlabel("Frequency (%)")

# -----------------------------
# Fix wind direction axis (degrees + labels)
# -----------------------------
angles_deg = [0, 45, 90, 135, 180, 225, 270, 315]
angles_rad = np.deg2rad(angles_deg)
labels = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

ax.set_xticks(angles_rad)
ax.set_xticklabels(labels)
ax.set_xlabel("Wind Direction")

ax.set_title(
    "3D Polar Wind Direction–Speed–Frequency Distribution (2017–18)"
)
plt.savefig(
    "../plots/3d_polar_wind_direction_speed_frequency_2017_18.png",
    dpi=300,
    pad_inches=0.4
)
ax.zaxis.labelpad = 10
plt.show()
