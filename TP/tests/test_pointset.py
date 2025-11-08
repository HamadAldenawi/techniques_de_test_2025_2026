import pytest
from TP.pointset import PointSet

def test_empty_pointset():
    points = []
    ps = PointSet(points)
    data = ps.to_bytes()
    ps2 = PointSet.from_bytes(data)
    assert ps2.points == []

def test_single_point():
    points = [(1, 2)]
    ps = PointSet(points)
    data = ps.to_bytes()
    ps2 = PointSet.from_bytes(data)
    assert ps2.points[0][0] == pytest.approx(1)
    assert ps2.points[0][1] == pytest.approx(2)

def test_multiple_points():
    points = [(0, 0), (1, 1), (2.5, -3.2)]
    ps = PointSet(points)
    data = ps.to_bytes()
    ps2 = PointSet.from_bytes(data)
    for p1, p2 in zip(points, ps2.points):
        assert p2[0] == pytest.approx(p1[0])
        assert p2[1] == pytest.approx(p1[1])

def test_negative_points():
    points = [(-1, -1), (-5.5, 3.2)]
    ps = PointSet(points)
    data = ps.to_bytes()
    ps2 = PointSet.from_bytes(data)
    for p1, p2 in zip(points, ps2.points):
        assert p2[0] == pytest.approx(p1[0])
        assert p2[1] == pytest.approx(p1[1])


        
