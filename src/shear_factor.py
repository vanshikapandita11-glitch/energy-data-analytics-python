import pandas as pd
import numpy as np

# Load 2018-19 data
df = pd.read_csv(
    "../data/wind_data_2018_19.txt",
    sep=None,
    engine="python",
    encoding="latin1",
    skiprows=15
)

# Drop empty column if present
df = df.dropna(axis=1, how="all")

# Select wind speed columns
v20 = df["20m Avg [m/s]"].dropna()
v50 = df["50m Avg [m/s]"].dropna()
v80 = df["80m Avg [m/s]"].dropna()

# Use North boom for 100m
v100 = df["100m_N Avg [m/s]"].dropna()

# Annual mean speeds
V20 = v20.mean()
V50 = v50.mean()
V80 = v80.mean()
V100 = v100.mean()

print("Annual mean wind speeds:")
print("20 m:", round(V20, 3))
print("50 m:", round(V50, 3))
print("80 m:", round(V80, 3))
print("100 m:", round(V100, 3))

# Shear factor function
def shear(V1, V2, H1, H2):
    return np.log(V2 / V1) / np.log(H2 / H1)

alpha_20_80 = shear(V20, V80, 20, 80)
alpha_50_100 = shear(V50, V100, 50, 100)

print("\nShear factor:")
print("α (20m–80m):", round(alpha_20_80, 3))
print("α (50m–100m):", round(alpha_50_100, 3))
