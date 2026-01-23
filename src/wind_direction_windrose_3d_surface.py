import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Frequency values (from your 2D wind rose)
# Order: N, NE, E, SE, S, SW, W, NW
# -----------------------------
freq = np.array([21, 9, 13, 5, 7, 30, 15, 6])  # use your actual % values

# Convert to fraction for smooth surface
freq = freq / max(freq)

# Angles
theta = np.linspace(0, 2*np.pi, 8, endpoint=False)
theta = np.append(theta, theta[0])

# Radius grid
r = np.linspace(0, 1, 50)
theta_grid, r_grid = np.meshgrid(theta, r)

# Create height surface
z = np.zeros_like(theta_grid)
for i in range(len(freq)):
    z[:, i] = freq[i]

# Convert polar to Cartesian
x = r_grid * np.cos(theta_grid)
y = r_grid * np.sin(theta_grid)

# -----------------------------
# Plot
# -----------------------------
fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111, projection="3d")

ax.plot_surface(
    x, y, z,
    cmap="Blues",
    edgecolor="k",
    alpha=0.9
)

ax.set_title("3D Wind Direction Frequency Wind Rose (2017–18)")
ax.set_zlabel("Relative Frequency")

ax.set_xticks([])
ax.set_yticks([])

plt.savefig(
    "../plots/3d_circular_windrose_surface_2017_18.png",
    dpi=300
)

plt.show()
