import pytest
from TP.triangulator.binary import (
    encode_pointset, decode_pointset,
    encode_triangles, decode_triangles
)
from TP.pointset import PointSet

def test_encode_decode_triangles():
    ps = PointSet([(0,0), (1,0), (0,1)])
    triangles = [(0,1,2)]
    blob = encode_triangles(ps, triangles)
    ps2, tris2 = decode_triangles(blob)
    assert ps2.to_list() == ps.to_list()
    assert tris2 == triangles

def test_decode_triangles_missing_section():
    ps = PointSet([(1,2),(3,4)])
    blob = encode_pointset(ps)
    ps2, tris = decode_triangles(blob)
    assert ps2.to_list() == ps.to_list()
    assert tris == []

def test_decode_pointset_small_buffer():
    with pytest.raises(ValueError):
        decode_pointset(b"\x00\x01")

def test_decode_triangles_corrupted():
    ps = PointSet([(1,1)])
    blob = encode_triangles(ps, [(0,0,0)])
    corrupted = blob[:-4]
    with pytest.raises(ValueError):
        decode_triangles(corrupted)
def test_decode_pointset_invalid_buffer():
    with pytest.raises(ValueError):
        decode_pointset(b"\x00\x00")  # أقل من 4 bytes
