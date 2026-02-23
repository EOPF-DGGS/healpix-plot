from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

import healpix_geo

if TYPE_CHECKING:
    from typing import Literal

    from healpix_plotting.ellipsoid import EllipsoidLike


class HealpixGridParameters(TypedDict):
    level: int
    indexing_scheme: Literal["nested", "ring", "zuniq"]
    ellipsoid: EllipsoidLike


@dataclass
class HealpixGrid:
    # FIXME: move the grid info objects out of `xdggs` and use that?
    level: int
    indexing_scheme: Literal["nested", "ring", "zuniq"]
    ellipsoid: EllipsoidLike = "sphere"

    def __post_init__(self):
        known_schemes = ["nested", "ring", "zuniq"]
        if self.indexing_scheme not in known_schemes:
            raise ValueError(f"unknown indexing scheme: {self.indexing_scheme}")

        if self.level not in range(0, 29 + 1):
            raise ValueError(
                f"level is outside the valid range of [0, 29]: {self.level}"
            )

    def as_keyword_params(self):
        return {"depth": self.level, "ellipsoid": self.ellipsoid}

    @property
    def operations(self):
        return getattr(healpix_geo, self.indexing_scheme)
