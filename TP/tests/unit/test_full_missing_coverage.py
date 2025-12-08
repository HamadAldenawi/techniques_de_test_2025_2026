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
# binary.py – cover missing lines 59 & 65
# ============================================================

def test_decode_triangles_no_triangles_section():
    # count=1, point x,y → no triangles after pointset
    data = struct.pack(">Iff", 1, 1.0, 2.0)
    ps, tris = decode_triangles(data)

    assert ps.points == [(1.0, 2.0)]
    assert tris == []  # covers line 59 + 65


def test_decode_triangles_incomplete_triangle_data():
    # 1 point + tcount=2 but no triangle bytes provided
    data = struct.pack(">IffI", 1, 1.0, 2.0, 2)

    with pytest.raises(ValueError):
        decode_triangles(data)  # covers line 65 (buffer too short)


# ============================================================
# client_psm.py – cover line 18
# ============================================================

def test_client_psm_error_status():
    client = PointSetManagerClient("http://fake")

    mock_resp = MagicMock()
    mock_resp.status_code = 404

    with patch("requests.get", return_value=mock_resp):
        with pytest.raises(RuntimeError):
            client.get_pointset(10)  # covers line 18


# ============================================================
# server.py – cover line 45
# ============================================================

def test_server_triangulate_exception():
    class FakeClient:
        def get_pointset(self, ps_id):
            raise Exception("boom")

    with patch.object(srv, "client", FakeClient()):
        client = app.test_client()
        rv = client.get("/triangulate/99")
        assert rv.status_code == 502   # covers line 45


# ============================================================
# triangulation.py – cover lines 28, 58–59
# ============================================================

def test_triangulation_less_than_three_points():
    assert triangulate([]) == []
    assert triangulate([(1, 2)]) == []
    assert triangulate([(1, 2), (3, 4)]) == []  # covers line 28


def test_triangulation_no_ear_found_break():
    # bow-tie shape where ear clipping fails → triggers break at lines 58-59
    pts = [(0, 0), (1, 1), (0, 1), (1, 0)]
    tris = triangulate(pts)
    assert isinstance(tris, list)  # covers lines 58–59
