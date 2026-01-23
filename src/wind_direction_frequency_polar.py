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

# Wind direction data
direction = df["78m WV [°]"].dropna()

# -------------------------
# Direction bins (8 sectors)
# -------------------------
bins = np.arange(0, 361, 45)   # 0,45,90,...,360
direction_bins = pd.cut(
    direction,
    bins=bins,
    include_lowest=True,
    right=False
)

# Map bin centre to direction label
def dir_label(interval):
    centre = (interval.left + interval.right) / 2
    mapping = {
        22.5: "N", 67.5: "NE", 112.5: "E", 157.5: "SE",
        202.5: "S", 247.5: "SW", 292.5: "W", 337.5: "NW"
    }
    return mapping.get(centre, "N")

direction_labels = direction_bins.apply(dir_label)

# Frequency calculation
freq = direction_labels.value_counts(normalize=True) * 100
freq = freq.reindex(["N", "NE", "E", "SE", "S", "SW", "W", "NW"])

# -------------------------
# Polar plot
# -------------------------
angles = np.deg2rad([0, 45, 90, 135, 180, 225, 270, 315])

fig = plt.figure(figsize=(6, 6))
ax = plt.subplot(111, polar=True)

ax.bar(
    angles,
    freq.values,
    width=np.deg2rad(45),
    align="center"
)

ax.set_xticks(angles)
ax.set_xticklabels(["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
ax.set_title("Wind Direction Frequency Distribution (2017–18)", pad=15)

plt.savefig(
    "../plots/wind_direction_frequency_polar_2017_18.png",
    dpi=300
)

plt.show()
