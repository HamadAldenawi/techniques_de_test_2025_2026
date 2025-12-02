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


def test_pointset_getitem():
    ps = PointSet([(10, 20), (30, 40)])
    assert ps[0] == (10, 20)
    assert ps[1] == (30, 40)
