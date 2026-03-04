---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  name: python3
  display_name: Python 3
---

# Quickstart

This guide shows how to plot a HEALPix dataset in three steps:

1. Define the grid
2. Create `cell_ids` and associated data
3. Plot the map

## Setup

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import healpix_plotting
```

## Step 1 — Define the HEALPix grid

HEALPix resolution is controlled by the **level** parameter.

The total number of cells is:

N=12×4^level

```{code-cell} python
child_level = 3
n_cells = 12 * 4**child_level

print(f"Level: {child_level}")
print(f"Number of cells: {n_cells}")
```

`level=3` gives **768 cells** - small enough for fast visualisation.

## Step 2 — Build cell IDs and data

In real workflows your `cell_ids` and `data` come from a file (NetCDF, Zarr, …). Here we generate a synthetic wave pattern.

```{code-cell} python
cell_ids = np.arange(n_cells)
data = np.random.rand(n_cells)

print(f"data shape: {data.shape}")
print(f"value range: [{data.min():.2f}, {data.max():.2f}]")
```

## Step 3 — plot

```{code-cell} python
fig, ax = plt.subplots(
    1, 1, subplot_kw={"projection": ccrs.Mollweide()}, figsize=(12, 12)
)

mappable = healpix_plotting.plot(
    cell_ids,
    data,
    healpix_grid={
        "level": child_level,
        "indexing_scheme": "nested",
        "ellipsoid": "WGS84",
    },
    sampling_grid={"shape": 400},
    ax=ax,
)

fig.colorbar(mappable, orientation="horizontal")
ax = mappable.figure.axes[0]

ax.coastlines()
ax.gridlines(draw_labels="x")
ax.gridlines(draw_labels="y")

plt.show()
```

## Result

You now have a global HEALPix map rendered on a Mollweide projection.

The plotting function:

- resamples HEALPix cells to a regular grid
- interpolates values
- renders the image on a Cartopy projection
