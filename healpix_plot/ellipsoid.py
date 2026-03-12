from typing import NotRequired, Protocol, TypedDict


class SphereDict(TypedDict):
    name: NotRequired[str]
    radius: float


class SphereType(Protocol):
    radius: float


class EllipsoidDict(TypedDict):
    name: NotRequired[str]
    semimajor_axis: float
    inverse_flattening: float


class EllipsoidType(Protocol):
    semimajor_axis: float
    inverse_flattening: float


# TODO: add to healpix-geo
EllipsoidLike = str | SphereDict | SphereType | EllipsoidDict | EllipsoidType
