import pytest
import struct
from unittest.mock import patch, MagicMock

from TP.pointset import PointSet
from TP.triangulator.binary import decode_triangles
from TP.triangulator.client_psm import PointSetManagerClient
from TP.triangulator import server as srv
from TP.triangulator.server import app
from TP.triangulator.triangulation import triangulate


# ============================================================
# 1) binary.py — cover lines 59 & 65
# ============================================================

def test_decode_triangles_no_triangle_section():
    data = struct.pack(">Iff", 1, 1.0, 2.0)
    ps, tris = decode_triangles(data)

    assert ps.points == [(1.0, 2.0)]
    assert tris == []   # covers line 59 + line 65


def test_decode_triangles_incomplete_triangle_data():
    data = struct.pack(">IffI", 1, 1.0, 2.0, 1)
    with pytest.raises(ValueError):
        decode_triangles(data)   # covers line 65 error case



# ============================================================
# 2) client_psm.py — cover line 18 (non-200 status)
# ============================================================

def test_client_psm_error_status():
    client = PointSetManagerClient("http://fake")

    fake = MagicMock()
    fake.status_code = 404

    with patch("requests.get", return_value=fake):
        with pytest.raises(RuntimeError):
            client.get_pointset(1)   # covers line 18



# ============================================================
# 3) server.py — cover line 45 (triangulate crashes)
# ============================================================

def test_server_triangulate_failure():
    class BadClient:
        def get_pointset(self, pid):
            raise Exception("bad")

    with patch.object(srv, "client", BadClient()):
        c = app.test_client()
        res = c.get("/triangulate/10")

        assert res.status_code == 502   # covers line 45



# ============================================================
# 4) triangulation.py — cover lines 28, 58–59, 68
# ============================================================

def test_triangulation_less_than_three():
    assert triangulate([]) == []
    assert triangulate([(0, 0)]) == []
    assert triangulate([(0, 0), (1, 1)]) == []   # covers line 28


def test_triangulation_no_ear_found():
    pts = [(0, 0), (1, 1), (0, 1), (1, 0)]   # bow-tie
    tris = triangulate(pts)
    assert isinstance(tris, list)   # covers lines 58–59 (break)


def test_triangulation_final_triangle():
    pts = [(0, 0), (1, 0), (0.5, 0.7), (0.3, 0.2)]
    tris = triangulate(pts)
    assert any(len(t) == 3 for t in tris)   # covers line 68
