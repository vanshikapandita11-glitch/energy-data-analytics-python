import pandas as pd

df = pd.read_csv(
    "../data/wind_data_2017_18.txt",
    sep=None,
    engine="python",
    encoding="latin1"
)

df = df.drop(columns=["Unnamed:17"], errors="ignore")

heights = {
    "20 m": ("20m Avg [m/s]", "20m Std [m/s]"),
    "50 m": ("50m Avg [m/s]", "50m Std [m/s]"),
    "80 m": ("80m Avg [m/s]", "80m Std [m/s]"),
    "100 m": ("100m_S Avg [m/s]", "100m_S Std [m/s]")
}

print("\nTurbulence Intensity (TI) at different heights:\n")

for height, (avg_col, std_col) in heights.items():
    mean_speed = df[avg_col]
    std_speed = df[std_col]

    TI = (std_speed / mean_speed).dropna()
    print(f"{height}: {TI.mean():.3f}")