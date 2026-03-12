import pytest

from healpix_plot import healpix


class TestHealpixGrid:
    @pytest.mark.parametrize("level", (3, 6, 29))
    @pytest.mark.parametrize("indexing_scheme", ["nested", "zuniq"])
    @pytest.mark.parametrize("ellipsoid", ["WGS84", "sphere", {"radius": 6371000.0}])
    def test_init(self, level, indexing_scheme, ellipsoid):
        actual = healpix.HealpixGrid(
            level=level, indexing_scheme=indexing_scheme, ellipsoid=ellipsoid
        )
        assert actual.level == level
        assert actual.indexing_scheme == indexing_scheme
        assert actual.ellipsoid == ellipsoid

    @pytest.mark.parametrize(
        ["level", "indexing_scheme"],
        (
            (1, "unknown"),
            (-1, "ring"),
        ),
    )
    def test_init_error(self, level, indexing_scheme):
        with pytest.raises(ValueError):
            healpix.HealpixGrid(
                level=level, indexing_scheme=indexing_scheme, ellipsoid="sphere"
            )

    @pytest.mark.parametrize("level", (3, 6, 29))
    @pytest.mark.parametrize("ellipsoid", ["WGS84", "sphere", {"radius": 6371000.0}])
    def test_as_keyword_params(self, level, ellipsoid):
        grid = healpix.HealpixGrid(
            level=level, indexing_scheme="nested", ellipsoid=ellipsoid
        )
        actual = grid.as_keyword_params()
        expected = {"depth": level, "ellipsoid": ellipsoid}

        assert actual == expected
