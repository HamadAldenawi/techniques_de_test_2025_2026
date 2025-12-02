from TP.triangulator.binary import encode_pointset, decode_pointset
from TP.pointset import PointSet
import pytest



def test_binary_encoding():
    ps = PointSet([(1.0, 2.0), (3.0, 4.0)])
    data = encode_pointset(ps)
    result = decode_pointset(data)
    assert len(result) == 2
    assert result[0] == (1.0, 2.0)
    assert result[1] == (3.0, 4.0)


def test_encode_decode_pointset_precision():
    ps = PointSet([(0.123456, 0.654321)])
    encoded = encode_pointset(ps)
    decoded = decode_pointset(encoded)
    x1, y1 = ps.points[0]
    x2, y2 = decoded.points[0]
    assert abs(x1 - x2) < 1e-5
    assert abs(y1 - y2) < 1e-5


# ------------------------------------------------------
#  TEST 1 — PointSet vide
# ------------------------------------------------------
def test_binary_empty_pointset():
    ps = PointSet([])
    encoded = encode_pointset(ps)
    decoded = decode_pointset(encoded)

    assert isinstance(decoded, PointSet)
    assert decoded.points == []


# ------------------------------------------------------
#  TEST 2 — PointSet grande (100 points)
# ------------------------------------------------------
def test_binary_large_pointset():
    ps = PointSet([(i * 0.1, i * 0.2) for i in range(100)])
    encoded = encode_pointset(ps)
    decoded = decode_pointset(encoded)

    assert len(decoded) == 100
    for (x1, y1), (x2, y2) in zip(ps.points, decoded.points):
        assert abs(x1 - x2) < 1e-5
        assert abs(y1 - y2) < 1e-5


# ------------------------------------------------------
# TEST 3 — Data must be bytes
# ------------------------------------------------------
def test_binary_output_type():
    ps = PointSet([(1, 2)])
    encoded = encode_pointset(ps)
    assert isinstance(encoded, bytes)

# ------------------------------------------------------
# TEST 4 — Buffer trop court (should raise error)
# ------------------------------------------------------
def test_binary_short_buffer_error():
    with pytest.raises(ValueError):
        decode_pointset(b"\x00\x00")  # أقل من 4 bytes → يجب أن يعطي خطأ


# ------------------------------------------------------
# TEST 5 — Negative and large float values
# ------------------------------------------------------
def test_binary_negative_and_large_values():
    ps = PointSet([
        (-1234.567, 9876.543),
        (1e10, -1e-9)
    ])
    encoded = encode_pointset(ps)
    decoded = decode_pointset(encoded)

    for (x1, y1), (x2, y2) in zip(ps.points, decoded.points):
        assert abs(x1 - x2) < 1e-3   # float32 دقة أقل للقيم الكبيرة
        assert abs(y1 - y2) < 1e-3


# ------------------------------------------------------
# TEST 6 — Corrupted binary data
# ------------------------------------------------------
def test_binary_corrupted_data():
    ps = PointSet([(1.0, 1.0)])
    encoded = encode_pointset(ps)

    # نفس طول البداية لكن نحذف جزء من البيانات (تلف)
    corrupted = encoded[:5]

    with pytest.raises(ValueError):
        decode_pointset(corrupted)