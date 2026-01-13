import pandas as pd
import matplotlib.pyplot as plt

# Load 2018–19 data
df = pd.read_csv(
    "../data/wind_data_2018_19.txt",
    sep=None,
    engine="python",
    encoding="latin1",
    skiprows=15
)

# Drop useless column if present
df = df.dropna(axis=1, how="all")

print("Columns:", df.columns.tolist())


# Use wind direction at 78 m (closest to 80 m hub height)
wind_dir = df["78m WV [°]"].dropna()

# Convert degrees to compass sectors
def to_sector(angle):
    if angle >= 337.5 or angle < 22.5:
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

sectors = wind_dir.apply(to_sector)

# Frequency distribution
freq = sectors.value_counts(normalize=True) * 100

print("Wind Direction Frequency (%)")
print(freq)

# Plot
plt.figure(figsize=(6,4))
freq.plot(kind="bar")
plt.title("Wind Direction Frequency (78m) 2018–19")
plt.ylabel("Percentage (%)")
plt.tight_layout()
plt.savefig("../plots/wind_direction_2018_19.png")
plt.show()
