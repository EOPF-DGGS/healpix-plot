from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal

    from healpix_plotting.ellipsoid import EllipsoidLike


@dataclass
class HealpixGrid:
    level: int
    indexing_scheme: Literal["nested", "ring", "zuniq"]
    ellipsoid: EllipsoidLike
