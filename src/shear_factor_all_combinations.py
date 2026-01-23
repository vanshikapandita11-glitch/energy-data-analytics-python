import pandas as pd
import numpy as np

df = pd.read_csv(
    "../data/wind_data_2017_18.txt",
    sep=None,
    engine="python",
    encoding="latin1"
)

df = df.drop(columns=["Unnamed: 17"], errors="ignore")

V20 = df["20m Avg [m/s]"].mean()
V50 = df["50m Avg [m/s]"].mean()
V80 = df["80m Avg [m/s]"].mean()
V100 = df["100m_S Avg [m/s]"].mean()

def shear(V1, V2, H1, H2):
    return np.log(V2 / V1) / np.log(H2 / H1)

results = {
    "20-50 m": shear(V20, V50, 20, 50),
    "50-80 m": shear(V50, V80, 50, 80),
    "80-100 m": shear(V80, V100, 80, 100),
    "50-100 m": shear(V50, V100, 50, 100),
    "20-80 m": shear(V20, V80, 20, 80),
    "50-100 m": shear(V50, V100, 50, 100),
    "20-100 m": shear(V20, V100, 20,100),
}

print("\nShear factor (α) for different height combinations:\n")
for k, v in results.items():
    print(f"{k}: {v:.3f}")