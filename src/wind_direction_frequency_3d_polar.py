import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(
    "../data/wind_data_2017_18.txt",
    sep=None,
    engine="python",
    encoding="latin1"
)

df = df.drop(columns=["Unnamed: 17"], errors="ignore")

# Wind direction column
direction = df["78m WV [°]"].dropna()

# -----------------------------
# Direction sector assignment
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

dir_data = direction.apply(lambda x: pd.Series(direction_sector(x)))
dir_data.columns = ["Dir", "Angle"]

# -----------------------------
# Frequency calculation
# -----------------------------
freq = dir_data["Dir"].value_counts(normalize=True) * 100
freq = freq.reindex(["N","NE","E","SE","S","SW","W","NW"])

angles = np.deg2rad([0,45,90,135,180,225,270,315])
heights = freq.values

# -----------------------------
# 3D Circular Plot
# -----------------------------
fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111, projection="3d")

theta = angles
r = np.ones_like(theta)          # fixed radius (visual only)
z = np.zeros_like(theta)
dz = heights

dtheta = np.deg2rad(45) * 0.85
dr = 0.4

ax.bar3d(theta, r, z, dtheta, dr, dz)

# Axis labels
ax.set_xticks(angles)
ax.set_xticklabels(["N","NE","E","SE","S","SW","W","NW"])
ax.set_xlabel("Wind Direction")
ax.set_zlabel("Frequency (%)")

# Remove meaningless Y axis
ax.set_yticks([])
ax.set_ylabel("")

ax.set_title("3D Wind Direction Frequency Distribution (2017–18)", pad=15)

# Save figure
plt.savefig(
    "../plots/3d_wind_direction_frequency_2017_18.png",
    dpi=300
)

plt.show()
