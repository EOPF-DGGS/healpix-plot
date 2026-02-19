from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from typing import Literal

    from healpix_plotting.healpix import HealpixGrid
    from healpix_plotting.sampling_grid import SamplingGrid


def resample(
    cell_ids: np.ndarray,
    data: np.ndarray,
    *,
    sampling_grid: SamplingGrid,
    healpix_grid: HealpixGrid,
    interpolation: Literal["nearest", "bilinear"],
    agg: Literal["mean", "median", "std", "var"],
) -> np.ndarray:
    pass
