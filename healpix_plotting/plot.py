from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from typing import Any, Literal

    import cartopy.crs as ccrs
    from matplotlib.axis import Axis
    from matplotlib.cm import ColorMap
    from matplotlib.norm import Norm

    from healpix_plotting.healpix import HealpixGrid
    from healpix_plotting.sampling_grid import SamplingGrid, SamplingGridParameters


def plot(
    cell_ids: np.ndarray,
    data: np.ndarray,
    *,
    healpix_grid: HealpixGrid,
    sampling_grid: SamplingGridParameters | SamplingGrid,
    projection: str | ccrs.CRS,
    agg: str = "mean",
    interpolation: str = "bilinear",
    rgb_clip: tuple[float, float] = (0.0, 1.0),
    ax: Axis | None = None,
    title: str | None = None,
    colorbar: bool | dict[str, Any] = False,
    cmap: str | ColorMap = "viridis",
    vmin: float | None = None,
    vmax: float | None = None,
    norm: Norm | None = None,
    axis_labels: dict[str, str] | Literal["none"] | None = None,
) -> Axis:
    pass
