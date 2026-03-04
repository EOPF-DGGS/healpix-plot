# Sampling grids

The sampling grid defines the regular pixel grid onto which HEALPix data is resampled before being rendered by Matplotlib. It controls the spatial extent, pixel resolution, and output image shape.

## Dict shorthand

Pass a plain dict with a `shape`:

```python
healpix_plotting.plot(..., sampling_grid={"shape": 1024})  # 1024x1024
healpix_plotting.plot(..., sampling_grid={"shape": (2048, 1024)})  # width x height
```

The spatial extent and pixel resolution are inferred automatically from the bounding box of your `cell_ids`.

## Bounding box

Use `SamplingGrid.from_bbox()` to pin the output to a fixed region regardless of the data:

```python
sampling_grid = healpix_plotting.SamplingGrid.from_bbox(
    bbox=(-15, 35, 40, 72),  # (lon_min, lat_min, lon_max, lat_max) in degrees
    shape=1024,
)
```

This is the right choice when comparing multiple datasets or animating over time.

## Affine transform (align with a reference raster)

Use `AffineSamplingGrid` when the output pixels must align with a reference raster
(e.g. a GeoTIFF):

```python
from healpix_plotting.sampling_grid import AffineSamplingGrid
from affine import Affine

transform = Affine(0.01, 0, -10, 0, -0.01, 60)  # 0.01 deg/pixel, top-left at (-10, 60)
sampling_grid = AffineSamplingGrid.from_transform(transform, shape=(4000, 2500))
```

## Background value

Pixels outside the coverage of your `cell_ids` are filled with `background_value`
(default: `numpy.nan`):

```python
healpix_plotting.plot(..., background_value=0.0)
```
