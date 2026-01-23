import pandas as pd
import numpy as np

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

data = df[["80m Avg [m/s]", "78m WV [°]"]].dropna()
data.columns = ["Speed", "Direction"]

# -----------------------------
# Wind direction bins (8 sectors)
# Centres: 0, 45, 90, ... 315
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

data[["Dir", "Dir_Centre"]] = data["Direction"].apply(
    lambda x: pd.Series(direction_sector(x))
)

# -----------------------------
# Wind speed bins
# Centres: 0.5, 1.0, 1.5, ...
# -----------------------------
speed_edges = np.arange(0.25, data["Speed"].max() + 0.75, 0.5)

data["Speed_Bin"] = pd.cut(
    data["Speed"],
    bins=speed_edges,
    include_lowest=True
)

# Calculate bin centre from bin edges
data["Speed_Centre"] = data["Speed_Bin"].apply(
    lambda x: round((x.left + x.right) / 2, 2)
)

# -----------------------------
# Frequency table
# -----------------------------
table = (
    data
    .groupby(["Dir", "Dir_Centre", "Speed_Centre"])
    .size()
    .reset_index(name="Count")
)

total_records = len(data)
table["Frequency (%)"] = table["Count"] / total_records * 100

# Remove zero-count rows
table = table[table["Count"] > 0]

# Sort for readability
table = table.sort_values(
    by=["Dir_Centre", "Speed_Centre"]
)

# -----------------------------
# Output checks
# -----------------------------
print(table.head(10))
print("\nCHECK:")
print("Total Frequency (%):", round(table["Frequency (%)"].sum(), 3))
