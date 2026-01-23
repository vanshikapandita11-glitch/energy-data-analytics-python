import pandas as pd
import numpy as np

df = pd.read_csv(
    "../data/wind_data_2017_18.txt",
    sep=None,
    engine="python",
    encoding="latin1"
)

df = df.drop(columns=["Unnamed: 17"], errors="ignore")

wind_speed = df["80m Avg [m/s]"]
wind_dir = df["78m WV [°]"]

data = pd.DataFrame({
    "speed": wind_speed,
    "direction": wind_dir
}).dropna()

total_records = len(data)

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
    
bin_width = 0.5
min_speed = np.floor(data["speed"].min())
max_speed = np.ceil(data["speed"].max())

speed_bins = np.arange(min_speed, max_speed + bin_width, bin_width)

data["Speed_Bin"] = pd.cut(
        data["speed"],
        bins=speed_bins,
        right=False
    )

table = (
        data
        .groupby(["Dir", "Angle", "Speed_Bin"])
        .size()
        .reset_index(name="Count")
    )

table["Frequency (%)"] = (table["Count"] / total_records) * 100
    
table = table.sort_values(["Angle", "Speed_Bin"]).reset_index(drop=True)

print(table)
print("\nCHECK:")
print("Total Frequency (%):", table["Frequency (%)"].sum())
# Remove zero-frequency rows for PPT table
ppt_table = table[table["Frequency (%)"] > 0]

print("\nPPT READY TABLE:")
print(ppt_table)

# ----------------------------
# Save table for plotting
# -----------------------------
table.to_csv(
    "../data/wind_direction_speed_table_2017_18.csv",
    index=False
)

print("CSV saved: wind_direction_speed_table_2017_18.csv")
