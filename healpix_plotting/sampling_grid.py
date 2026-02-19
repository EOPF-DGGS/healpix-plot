from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

import numpy as np

if TYPE_CHECKING:
    from typing import Self

    import affine


class SamplingGridParameters(TypedDict):
    """Sampling parameters as a dict

    Parameters
    ----------
    shape : int or tuple of int, default: 1024
        The shape of the array. If a int, the shape is a square of equal size.
    resolution : float or tuple of float, optional
        The resolution or step size of the sampling grid. If a float, expands to
        a 2-tuple of equal values. If missing, derived from the spatial extent
        of the data and the given shape.
    center : tuple of float, optional
        The center of the sampling grid. If missing, this is inferred from the data.
    """

    shape: int | tuple[int, int] = 1024
    resolution: float | tuple[float, float] | None = None
    center: tuple[float, float] | None = None


@dataclass
class SamplingGrid:
    """materialized sampling grid"""

    x: np.ndarray
    y: np.ndarray

    @classmethod
    def from_transform(cls, transform: affine.Affine) -> Self:
        pass

    @classmethod
    def from_parameters(
        cls,
        shape: tuple[int, int],
        resolution: tuple[float, float],
        center: tuple[float, float],
    ) -> Self:
        pass

    @classmethod
    def from_bbox(cls, bbox: tuple[float, float, float, float]) -> Self:
        pass

    @classmethod
    def from_dict(cls, mapping: SamplingGridParameters) -> Self:
        pass
