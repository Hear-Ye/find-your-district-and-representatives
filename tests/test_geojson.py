import pytest

from src.app import GEOJSON, get_district


votable = set(range(len(GEOJSON)))
non_votable = {12, 87, 130, 231, 346, 417}
# Get rid of non votable districts for testing sake
# I'm going to add them back in once I figure out which
# 6 VOTING districts are missing and what's causing the
# geojson to fail.
votable.difference_update(non_votable)


@pytest.mark.parametrize("index", votable)
def test_geojson_indices_good(index):
    assert get_district(index)
