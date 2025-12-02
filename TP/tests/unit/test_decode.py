from TP.triangulator.binary import encode_pointset, decode_pointset
from TP.pointset import PointSet


def test_decode_zero_points():
    ps = PointSet([])
    encoded = encode_pointset(ps)
    decoded = decode_pointset(encoded)
    assert isinstance(decoded, PointSet)
    assert decoded.points == []


def test_decode_random():
    ps = PointSet([(1.5, -2.3), (0.0, 9.9)])
    encoded = encode_pointset(ps)
    decoded = decode_pointset(encoded)

    assert isinstance(decoded, PointSet)
    assert len(decoded.points) == len(ps.points)

    for (x1, y1), (x2, y2) in zip(decoded.points, ps.points):
        assert abs(x1 - x2) < 1e-5
        assert abs(y1 - y2) < 1e-5


# ------------------------------------------------------------
# TEST 1 — décode un seul point
# ------------------------------------------------------------
def test_decode_one_point():
    ps = PointSet([(10.0, -5.0)])
    encoded = encode_pointset(ps)
    decoded = decode_pointset(encoded)

    assert len(decoded.points) == 1
    x1, y1 = ps.points[0]
    x2, y2 = decoded.points[0]
    assert abs(x1 - x2) < 1e-5
    assert abs(y1 - y2) < 1e-5


# ------------------------------------------------------------
# TEST 2 — décode plusieurs points (test plus large)
# ------------------------------------------------------------
def test_decode_many_points():
    ps = PointSet([(i * 0.1, i * 0.2) for i in range(20)])
    encoded = encode_pointset(ps)
    decoded = decode_pointset(encoded)

    assert len(decoded.points) == 20
    for (x1, y1), (x2, y2) in zip(ps.points, decoded.points):
        assert abs(x1 - x2) < 1e-5
        assert abs(y1 - y2) < 1e-5


# ------------------------------------------------------------
# TEST 3 — le résultat doit être exactement un PointSet
# ------------------------------------------------------------
def test_decode_type_check():
    ps = PointSet([(1.0, 2.0), (3.0, 4.0)])
    encoded = encode_pointset(ps)
    decoded = decode_pointset(encoded)

    assert isinstance(decoded, PointSet)
    assert hasattr(decoded, "points")

