import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import weibull_min

# Wind data

df = pd.read_csv(
    "../data/wind_data_2017_18.txt",
    sep=None,
    engine="python",
    encoding="latin1"
)

df = df.drop(columns=["Unnamed: 17"], errors="ignore")

wind_speed = df["80m Avg [m/s]"].dropna()

# Weubull fitting
shape_k, loc, scale_c = weibull_min.fit(wind_speed, floc=0)

print("Weibull Parameters:")
print("Shape factor (k):", round(shape_k, 3))
print("Scale factor (c:)", round(scale_c, 3))

x = np.linspace(0, wind_speed.max(), 100)

plt.hist(wind_speed, bins=30, density=True, alpha=0.6, label="Observed data")
plt.plot(x, weibull_min.pdf(x, shape_k, loc, scale_c),
         'r-', label="Weibull fit")

plt.xlabel("Wind Speed (m/s)")
plt.ylabel("Frequency Distribution")
plt.title("Weibull Distribution Fit - Wind Speed at 80 m (2017-2018)")
plt.legend()
plt.grid(True)
plt.savefig("../plots/weibull_fit_2017_18.png", dpi=300, bbox_inches="tight")
plt.close()

