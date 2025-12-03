import pytest
from TP.pointset import PointSet


def test_pointset_basic():
    ps = PointSet([(0, 1), (2, 3)])
    assert len(ps) == 2
    assert ps[0] == (0, 1)
    assert ps.to_list() == [(0, 1), (2, 3)]

    d = ps.as_dict()
    assert "points" in d

    ps2 = PointSet.from_dict(d)
    assert ps2.to_list() == ps.to_list()


def test_pointset_from_dict_invalid():
    bad_data = {"points": "not a list"}

    # accepte ValueError ou TypeError
    with pytest.raises((ValueError, TypeError)):
        PointSet.from_dict(bad_data)


def test_pointset_index_out_of_bounds():
    ps = PointSet([(1, 2)])
    with pytest.raises(IndexError):
        _ = ps[5]


def test_pointset_negative_coordinates():
    ps = PointSet([(-1, -2), (3, -4)])
    assert ps.to_list() == [(-1, -2), (3, -4)]
