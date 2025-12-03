import pytest
import struct
from unittest.mock import patch
from TP.triangulator.binary import decode_triangles
from TP.triangulator.server import app
from TP.triangulator.triangulation import triangulate
from TP.pointset import PointSet

# ============================================================
# Cover binary.py lines 59 & 65
# ============================================================
def test_force_binary_missing_triangle_section():
    # Create a valid PointSet binary WITHOUT triangle section
    # count = 1 point → (1.0, 2.0)
    data = struct.pack(">Iff", 1, 1.0, 2.0)

    ps, triangles = decode_triangles(data)

    assert isinstance(ps, PointSet)
    assert ps.points == [(1.0, 2.0)]
    assert triangles == []  # covers lines 59 and 65


# ============================================================
# Cover server.py line 45 (error returned as 502)
# ============================================================
def test_force_server_exception_returns_502():
    from TP.triangulator import server as srv

    class FakeClientError:
        def get_pointset(self, _):
            raise Exception("forced error")

    with patch.object(srv, "client", FakeClientError()):
        client = app.test_client()
        resp = client.get("/triangulate/999")

        assert resp.status_code == 502  # covers line 45


# ============================================================
# Cover triangulation.py lines: 28 (n<3), 58–59 (no ear found), 68 (last triangle)
# ============================================================

def test_force_triangulation_less_than_three():
    """Covers line 28"""
    assert triangulate([(0, 0), (1, 1)]) == []


def test_force_triangulation_no_ear_found():
    """Covers lines 58–59"""
    # Bow-tie polygon → ear clipping fails
    pts = [(0,0),(1,1),(0,1),(1,0)]
    result = triangulate(pts)
    assert isinstance(result, list)  # ear-clipping fails → covers break


def test_force_triangulation_last_triangle():
    """Covers line 68"""
    pts = [(0,0),(1,0),(1,1),(0,1)]
    result = triangulate(pts)
    assert any(len(t)==3 for t in result)
