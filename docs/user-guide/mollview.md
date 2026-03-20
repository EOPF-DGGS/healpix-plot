# `healpix_mollview` — HEALPix Mollweide Visualisation

> A `healpy`-free replacement for `healpy.mollview` and `healpy.gnomview`,
> built on top of **healpix-geo** for all coordinate-system geometry.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Installation & Dependencies](#2-installation--dependencies)
3. [Quick Start](#3-quick-start)
4. [Public API](#4-public-api)
   - 4.1 [`mollview`](#41-mollview)
   - 4.2 [`mollgnomview`](#42-mollgnomview)
5. [Figure Layout — `hold` and `sub`](#5-figure-layout--hold-and-sub)
6. [RING vs NESTED pixel ordering](#6-ring-vs-nested-pixel-ordering)
7. [Ellipsoid support](#7-ellipsoid-support)
8. [Algorithm — how the rendering works](#8-algorithm--how-the-rendering-works)
   - 8.1 [Mollweide projection](#81-mollweide-projection)
   - 8.2 [Gnomonic projection](#82-gnomonic-projection)
9. [Internal helpers](#9-internal-helpers)
10. [Comparison with `healpy`](#10-comparison-with-healpy)
11. [Common recipes](#11-common-recipes)
12. [Known limitations](#12-known-limitations)

---

## 1. Overview

`healpix_mollview.py` provides two visualisation functions for HEALPix sky/sphere maps:

| Function | Projection | healpy equivalent |
|---|---|---|
| `mollview` | Mollweide (equal-area, full sky) | `healpy.mollview` |
| `mollgnomview` | Gnomonic (tangent-plane, local zoom) | `healpy.gnomview` |

Key differences from healpy:

- **No healpy dependency.** All HEALPix geometry is handled by [`healpix-geo`](https://github.com/EOPF-DGGS/healpix-geo) and `cdshealpix`.
- **Depth is inferred automatically** from the map size — you never pass it explicitly.
- **RING order by default**, like healpy. Pass `nest=True` for NESTED maps.
- **Non-spherical ellipsoids** (e.g. WGS84) are supported via healpix-geo.
- **No return value** — the function draws into the current matplotlib state, exactly like `healpy.mollview`. Use `plt.gcf()`, `plt.savefig()`, or `plt.show()` afterwards.
- **`hold` and `sub` parameters** control where the plot appears, mirroring healpy's interface.

---

## 2. Installation & Dependencies

```bash
pip install healpix-geo numpy matplotlib
```

`healpix-geo` pulls in `cdshealpix` automatically, which provides the
`to_ring` conversion used internally.

Python ≥ 3.10 is required (uses `X | Y` union type hints).

---

## 3. Quick Start

```python
import numpy as np
import matplotlib.pyplot as plt
from healpix_mollview import mollview, mollgnomview

# --- Synthetic RING map (depth 5, nside 32) ---
depth = 5
npix  = 12 * 4**depth          # 12 288 pixels
m     = np.random.default_rng(0).standard_normal(npix)

# Single full-sky view — new figure created automatically
mollview(m, title="My map", cmap="RdBu_r", unit="K")
plt.show()

# Local zoom centred on (lon=45°, lat=30°)
mollgnomview(m, lon_center=45.0, lat_center=30.0, fov_deg=20.0,
             title="Zoom 20°", cmap="plasma")
plt.show()
```

---

## 4. Public API

### 4.1 `mollview`

```python
mollview(
    hpx_map,
    *,
    nest         = False,
    title        = "",
    cmap         = "viridis",
    vmin         = None,
    vmax         = None,
    rot          = 0.0,
    ellipsoid    = "sphere",
    graticule    = True,
    graticule_step = 30.0,
    unit         = "",
    bgcolor      = "black",
    width_px     = 1600,
    height_px    = 800,
    norm         = None,
    bad_color    = "gray",
    flip         = "astro",
    figsize      = (14, 7),
    colorbar     = True,
    hold         = False,
    sub          = None,
) -> None
```

Renders a HEALPix map in the **Mollweide equal-area projection** (full sky).

#### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `hpx_map` | `np.ndarray`, shape `(12·4^depth,)` | — | Input HEALPix map. RING order by default; use `nest=True` for NESTED. |
| `nest` | `bool` | `False` | Pixel ordering of the input map. `False` = RING (healpy default). `True` = NESTED. |
| `title` | `str` | `""` | Title displayed above the map. |
| `cmap` | `str` or `Colormap` | `"viridis"` | Matplotlib colormap name or object. `"RdBu_r"` is recommended for CMB/temperature maps. |
| `vmin` | `float` or `None` | `None` | Lower bound of the colour scale. Defaults to the 2nd percentile of finite values. |
| `vmax` | `float` or `None` | `None` | Upper bound of the colour scale. Defaults to the 98th percentile of finite values. |
| `rot` | `float` | `0.0` | Central longitude of the map in degrees. `rot=180` centres the view on the 180° meridian. |
| `ellipsoid` | `str` | `"sphere"` | Reference ellipsoid used by healpix-geo for the lon/lat → pixel conversion. `"sphere"` gives results identical to healpy. Other supported values: `"WGS84"`, `"GRS80"`. |
| `graticule` | `bool` | `True` | Draw meridians and parallels. |
| `graticule_step` | `float` | `30.0` | Spacing of the graticule lines in degrees. |
| `unit` | `str` | `""` | Unit string shown below the colorbar. |
| `bgcolor` | `str` | `"black"` | Background colour outside the Mollweide ellipse. Any matplotlib colour string. |
| `width_px` | `int` | `1600` | Horizontal resolution of the rasterised image in pixels. Increase for high-depth maps (depth ≥ 8). |
| `height_px` | `int` | `800` | Vertical resolution of the rasterised image in pixels. |
| `norm` | `Normalize` or `None` | `None` | Custom matplotlib normalisation (e.g. `LogNorm()`). Overrides `vmin`/`vmax` when provided. |
| `bad_color` | `str` | `"gray"` | Colour used for `NaN` values in the map. |
| `flip` | `str` | `"astro"` | East/west convention. `"astro"`: east is to the left (astronomical convention). `"geo"`: east is to the right (geographical convention). |
| `figsize` | `(float, float)` | `(14, 7)` | Figure size in inches. Only used when a new figure is created (`hold=False` and `sub=None`). |
| `colorbar` | `bool` | `True` | Show a horizontal colorbar below the map. |
| `hold` | `bool` | `False` | If `True`, draw into the current axes (`plt.gca()`). If `False`, create a new figure. Ignored when `sub` is provided. |
| `sub` | `(int, int, int)` or `None` | `None` | `(nrows, ncols, index)` — place the map in a subplot of the current figure. Example: `sub=(1, 2, 1)`. Overrides `hold`. |

#### Returns

`None`. The function has no return value (same behaviour as `healpy.mollview`).
Access the current figure with `plt.gcf()`.

#### Raises

| Exception | Condition |
|---|---|
| `ValueError` | `hpx_map.size` is not of the form `12 · 4^depth` for any non-negative integer `depth`. |
| `ValueError` | `flip` is not `"astro"` or `"geo"`. |

---

### 4.2 `mollgnomview`

```python
mollgnomview(
    hpx_map,
    lon_center,
    lat_center,
    *,
    nest       = False,
    fov_deg    = 10.0,
    title      = "",
    cmap       = "viridis",
    vmin       = None,
    vmax       = None,
    ellipsoid  = "sphere",
    unit       = "",
    width_px   = 800,
    height_px  = 800,
    figsize    = (7, 7),
    colorbar   = True,
    hold       = False,
    sub        = None,
) -> None
```

Renders a local zoom in the **gnomonic (tangent-plane) projection**.  
The depth is inferred automatically from the map size.

#### Parameters specific to `mollgnomview`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `lon_center` | `float` | — | Longitude of the view centre in degrees. |
| `lat_center` | `float` | — | Latitude of the view centre in degrees. |
| `fov_deg` | `float` | `10.0` | Total field of view (square side) in degrees. |

All other parameters (`nest`, `cmap`, `vmin`, `vmax`, `ellipsoid`, `unit`,
`width_px`, `height_px`, `figsize`, `colorbar`, `hold`, `sub`) are identical
to those of `mollview`.

---

## 5. Figure Layout — `hold` and `sub`

The three modes below are mutually exclusive, with the priority order:
**`sub` > `hold=True` > `hold=False`**.

### New figure (default)

```python
mollview(m, title="My map")
plt.show()
```

A fresh `plt.figure()` is created each call. This is the same behaviour as
`healpy.mollview`.

### `hold=True` — reuse the current axes

```python
plt.figure(figsize=(14, 7))
ax = plt.gca()
# ... draw something on ax first ...
mollview(m, hold=True, title="Overlay")
plt.show()
```

The map is drawn into whichever axes is currently active.

### `sub=(nrows, ncols, idx)` — subplot grid

Place multiple maps in a single figure using standard matplotlib subplot
indexing. Rows and columns are 1-based.

```python
plt.figure(figsize=(18, 5), facecolor="black")
mollview(m1, sub=(1, 2, 1), title="Map A", cmap="plasma")
mollview(m2, sub=(1, 2, 2), title="Map B", cmap="RdBu_r")
plt.tight_layout()
plt.savefig("comparison.png", dpi=150, bbox_inches="tight", facecolor="black")
plt.close()
```

More complex layouts:

```python
plt.figure(figsize=(18, 10), facecolor="black")
mollview(m1, sub=(2, 3, 1), title="(1,1)")
mollview(m2, sub=(2, 3, 2), title="(1,2)")
mollview(m3, sub=(2, 3, 3), title="(1,3)")
mollview(m4, sub=(2, 3, 4), title="(2,1)")
mollview(m5, sub=(2, 3, 5), title="(2,2)")
mollview(m6, sub=(2, 3, 6), title="(2,3)")
plt.tight_layout()
plt.show()
```

---

## 6. RING vs NESTED pixel ordering

HEALPix maps can be stored in two pixel orderings:

| Ordering | Description | Default in |
|---|---|---|
| **RING** | Pixels ordered in iso-latitude rings, west to east | `healpy`, this module |
| **NESTED** | Pixels ordered along a space-filling (Z-order) curve within each base pixel | `healpix-geo` |

This module always uses RING order by default (`nest=False`), matching
`healpy.mollview`. The `nest` flag selects the ordering of the *input map*; the
internal healpix-geo calls always work in NESTED and the conversion
`NESTED → RING` is applied automatically using `cdshealpix.nested.to_ring`.

```python
# RING map (healpy default)
mollview(m_ring)

# NESTED map
mollview(m_nested, nest=True)

# Converting between orderings with healpy
import healpy as hp
m_nested = hp.reorder(m_ring,  r2n=True)
m_ring   = hp.reorder(m_nested, n2r=True)
```

---

## 7. Ellipsoid support

The `ellipsoid` parameter is forwarded directly to
`healpix_geo.nested.lonlat_to_healpix`. On a sphere (`ellipsoid="sphere"`,
the default), results are numerically identical to healpy. On a non-spherical
ellipsoid, the authalic latitude is used for the lon/lat → cell-ID conversion,
which is not possible with healpy.

```python
# Geographic data referenced to WGS84
mollview(m_ring, ellipsoid="WGS84", title="WGS84 Mollweide")

# Other supported ellipsoids (check healpix-geo documentation)
mollview(m_ring, ellipsoid="GRS80")
```

> **Note:** changing the ellipsoid only affects which HEALPix cell each
> image pixel maps to. The visual shape of the Mollweide projection is always
> the same mathematical ellipse regardless of the ellipsoid choice.

---

## 8. Algorithm — how the rendering works

### 8.1 Mollweide projection

The rendering pipeline is **image-first**: for each pixel in the output image,
we compute which HEALPix cell it falls in, then look up the map value. This
avoids HEALPix boundary artefacts and produces a smooth raster regardless of
resolution.

```
Output image grid (width_px × height_px)
           │
           ▼  _mollweide_inverse()          — analytic closed form
   (lon, lat) for each pixel  [degrees]
           │
           ▼  + longitude rotation (rot)
   (lon_rotated, lat)
           │
           ▼  lonlat_to_healpix()           — healpix-geo, NESTED output
   cell_id (NESTED)
           │
           ▼  _nested_to_ring() if nest=False
   cell_id (RING or NESTED)
           │
           ▼  hpx_map[cell_id]
   scalar value per pixel
           │
           ▼  matplotlib ScalarMappable     — normalise + colormap
   RGBA image  (height_px × width_px × 4)
           │
           ▼  ax.imshow + Ellipse patch + graticule
   Final figure
```

**Mollweide inverse formula** (pixel → lon/lat):

The normalised Mollweide coordinate system uses `x ∈ [-2, 2]`, `y ∈ [-1, 1]`
with the sphere inscribed in the ellipse `(x/2)² + y² ≤ 1`.

The auxiliary angle `θ` is obtained directly as `θ = arcsin(y)`, then:

```
sin(φ) = (2θ + sin(2θ)) / π        φ = geographic latitude
λ      = (x/2) · π / cos(θ)        λ = longitude offset
```

**Mollweide forward formula** (lon/lat → pixel, used for graticule lines):

Requires iterative Newton-Raphson to solve `2θ + sin(2θ) = π·sin(φ)`:

```
x = (2/π) · λ · cos(θ)
y = sin(θ)
```

Convergence is typically reached in fewer than 10 iterations to `tol=1e-12`.

### 8.2 Gnomonic projection

The gnomonic (tangent-plane) projection is centred on `(lon_center, lat_center)`.
Each image pixel corresponds to a direction in the tangent plane at angular
distance `ρ = arctan(r)` from the centre. The deprojection to geographic
coordinates uses the standard spherical gnomonic formulae:

```
φ = arcsin( cos(c)·sin(φ₀) + y·sin(c)·cos(φ₀)/ρ )
λ = λ₀ + arctan2( x·sin(c),  ρ·cos(φ₀)·cos(c) − y·sin(φ₀)·sin(c) )
```

where `c = arctan(ρ)` and `(φ₀, λ₀)` are the centre coordinates.

---

## 9. Internal helpers

These functions are not part of the public API (prefixed with `_`) but are
documented here for completeness.

| Function | Signature | Description |
|---|---|---|
| `_depth_from_npix` | `(npix: int) → int` | Infers HEALPix depth from the number of pixels. Raises `ValueError` for invalid sizes. |
| `_mollweide_inverse` | `(x, y) → (lon_deg, lat_deg)` | Analytic inverse Mollweide projection. Vectorised over arrays. |
| `_mollweide_forward` | `(lon_deg, lat_deg) → (x, y)` | Forward Mollweide via Newton-Raphson. Used for graticule lines. |
| `_make_mollweide_grid` | `(width, height) → (lon_grid, lat_grid, inside)` | Builds the full lon/lat grid for the image, plus the ellipse mask. |
| `_draw_graticule` | `(ax, step, rot, line_kwargs)` | Draws meridians and parallels on an Axes. |
| `_draw_graticule_labels` | `(ax, step, rot, color)` | Adds longitude labels along the bottom and latitude labels on the left. |

---

## 10. Comparison with `healpy`

| Feature | `healpy.mollview` | `mollview` (this module) |
|---|---|---|
| Pixel ordering | RING by default | RING by default (`nest=False`) |
| Depth/nside parameter | `mollview(m, ...)` with explicit nside inferred from map | Inferred automatically from `len(hpx_map)` |
| Rotation | `rot=(lon, lat, psi)` tuple | `rot=lon_deg` scalar |
| Ellipsoid | sphere only | `"sphere"` (default), `"WGS84"`, `"GRS80"`, … |
| Image resolution | fixed internal grid | configurable: `width_px`, `height_px` |
| Return value | `None` | `None` |
| `hold` / `sub` | supported | supported |
| healpy dependency | required | **not required** |
| NaN handling | `bad_color` | `bad_color` |
| Colour normalisation | `min`/`max` or percentile | percentiles 2/98 by default; custom `norm` supported |

### Migration from healpy

```python
# healpy
import healpy as hp
hp.mollview(m, title="My map", nest=False, cmap="RdBu_r", unit="K",
            min=-3, max=3)

# This module — drop-in equivalent
from healpix_mollview import mollview
mollview(m, title="My map", nest=False, cmap="RdBu_r", unit="K",
         vmin=-3, vmax=3)
```

The main parameter renames are: `min` → `vmin`, `max` → `vmax`.
The `rot` parameter accepts only a longitude scalar here (not a 3-tuple).

---

## 11. Common recipes

### Save to file (no display)

```python
import matplotlib
matplotlib.use("Agg")   # non-interactive backend — no window

from healpix_mollview import mollview
import matplotlib.pyplot as plt

mollview(m, title="My map", cmap="RdBu_r")
plt.savefig("map.png", dpi=150, bbox_inches="tight", facecolor="black")
plt.close()
```

### Custom colour normalisation (log scale)

```python
import matplotlib.colors as mcolors
from healpix_mollview import mollview

mollview(m_positive, norm=mcolors.LogNorm(vmin=1e-3, vmax=1.0),
         title="Log scale", cmap="inferno")
```

### Symmetric diverging scale

```python
import numpy as np
from healpix_mollview import mollview

absmax = np.nanpercentile(np.abs(m), 98)
mollview(m, vmin=-absmax, vmax=absmax, cmap="RdBu_r",
         title="Symmetric ±{:.2f}".format(absmax))
```

### Compare two maps side by side

```python
import matplotlib.pyplot as plt
from healpix_mollview import mollview

fig = plt.figure(figsize=(18, 5), facecolor="black")
mollview(m1, sub=(1, 2, 1), title="Map A", cmap="plasma", vmin=-3, vmax=3)
mollview(m2, sub=(1, 2, 2), title="Map B", cmap="plasma", vmin=-3, vmax=3)
plt.tight_layout()
plt.savefig("comparison.png", dpi=150, bbox_inches="tight", facecolor="black")
plt.close()
```

### Full-sky + local zoom in one figure

```python
import matplotlib.pyplot as plt
from healpix_mollview import mollview, mollgnomview

fig = plt.figure(figsize=(18, 8), facecolor="black")
mollview(m,     sub=(1, 2, 1), title="Full sky",   cmap="RdBu_r")
mollgnomview(m, lon_center=45.0, lat_center=30.0,
             fov_deg=20.0, sub=(1, 2, 2), title="Zoom 20°", cmap="RdBu_r")
plt.tight_layout()
plt.show()
```

### Geographical convention (east to the right), WGS84

```python
mollview(m, flip="geo", ellipsoid="WGS84",
         title="Geographic — WGS84", cmap="terrain")
```

### Convert a NESTED map before plotting

```python
# If you have a NESTED map and want to pass it as RING
import healpy as hp
m_ring = hp.reorder(m_nested, n2r=True)
mollview(m_ring, title="Converted to RING")

# Or simply pass it directly with nest=True
mollview(m_nested, nest=True, title="NESTED map")
```

### Increase image resolution for a high-depth map

```python
# depth=8 → nside=256 → 786 432 pixels
# Default 1600×800 may be too coarse; use 3200×1600
mollview(m_high_res, width_px=3200, height_px=1600,
         title="High-res map (depth=8)")
```

---

## 12. Known limitations

- **`rot` is a scalar longitude only.** Unlike `healpy.mollview` which accepts
  a 3-tuple `(lon, lat, psi)` for full rotation, only longitude rotation is
  supported here. Latitude rotation and roll are not implemented.

- **RING → NESTED conversion uses `cdshealpix`.** If you are using a very
  unusual nside that `cdshealpix` does not support, the conversion may fail.
  All standard power-of-two nside values (nside = 1, 2, 4, … 2^29) are
  supported.

- **No partial-sky maps.** The input must be a full-sky map of exactly
  `12 · 4^depth` pixels. Partial-sky (cut-sky) maps must be zero-padded or
  filled with `NaN` to full size before plotting.

- **Performance.** The rasterisation loop is vectorised over pixels with
  NumPy, but for `width_px × height_px ≥ 4 × 10^6` the call to
  `lonlat_to_healpix` may take a few seconds. Reduce the resolution or
  pre-cache the index grid if you need to render many maps at the same
  resolution.
