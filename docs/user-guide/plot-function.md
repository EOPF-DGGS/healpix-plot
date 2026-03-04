# The plot() function

{func}`healpix_plotting.plot` is the main entry point of the library. It resamples HEALPix data onto a regular pixel grid and renders it with Matplotlib and Cartopy.

## Minimal call

```python
healpix_plotting.plot(
    cell_ids,  # 1-D array of HEALPix cell IDs (uint64)
    data,  # 1-D scalar array, or (N, 3)/(N, 4) for RGB/RGBA
    healpix_grid=grid,  # HealpixGrid object (or dict)
    sampling_grid={"shape": 1024},
)
```

## Interpolation

```python
healpix_plotting.plot(..., interpolation="nearest")  # default
healpix_plotting.plot(
    ..., interpolation="bilinear"
)  # smoother, better for continuous fields
```

## Plot on an existing axis

When you pass `ax`, the `projection` parameter is ignored:

```python
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

fig, ax = plt.subplots(subplot_kw={"projection": ccrs.Robinson()})
healpix_plotting.plot(..., ax=ax)
plt.show()
```

## Title and axis labels

```python
healpix_plotting.plot(
    ...,
    title="Surface temperature",
    axis_labels={"x": "Longitude", "y": "Latitude"},
)
healpix_plotting.plot(..., axis_labels="none")  # hide labels
```

## RGB / RGBA data

Pass an `(N, 3)` or `(N, 4)` array (values in `[0, 1]`) to render a colour image.
`cmap`, `vmin`, `vmax`, and `norm` are ignored in RGB mode.

```python
data_rgb = np.stack([r, g, b], axis=1)  # shape (N, 3)
healpix_plotting.plot(..., data=data_rgb, rgb_clip=(0.0, 1.0))
```
