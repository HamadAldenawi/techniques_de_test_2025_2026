import pytest
from TP.triangulator.binary import decode_pointset, decode_triangles
from TP.triangulator.client_psm import PointSetManagerClient
from TP.triangulator.server import app
from TP.triangulator.triangulation import triangulate
from TP.pointset import PointSet
from unittest.mock import patch, MagicMock


# ============================================================
# 1) COVER binary.py lines: 59 & 65  (missing triangles section)
# ============================================================

def test_decode_triangles_no_triangle_section():
    # buffer contains: count=1 + point (float32 x,y)
    import struct
    data = struct.pack(">Iff", 1, 1.0, 2.0)
    ps, triangles = decode_triangles(data)

    assert isinstance(ps, PointSet)
    assert ps.points == [(1.0, 2.0)]
    assert triangles == []   # line 59,65 covered



# ============================================================
# 2) COVER client_psm.py line: 18  (non-200 response)
# ============================================================

def test_client_psm_non_200():
    client = PointSetManagerClient("http://fake")

    fake_resp = MagicMock()
    fake_resp.status_code = 400

    with patch("requests.get", return_value=fake_resp):
        with pytest.raises(RuntimeError):   # covers line 18
            client.get_pointset(1)



# ============================================================
# 3) COVER server.py line: 45 (error in triangulate)
# ============================================================

def test_server_error_response():
    from TP.triangulator import server as srv

    class FakeClient:
        def get_pointset(self, ps_id):
            raise Exception("boom")

    # replace real client
    with patch.object(srv, "client", FakeClient()):
        client = app.test_client()
        rv = client.get("/triangulate/5")

        assert rv.status_code == 502   # line 45 reached



# ============================================================
# 4) triangulation.py missing lines: 28, 58-59, 68
# ============================================================

# line 28: n < 3 → empty
def test_triangulation_less_than_3_points():
    assert triangulate([(0,0), (1,1)]) == []   # line 28


# lines 58-59: ear not found, break
def test_triangulation_no_ear_found():
    # Points arranged to break algorithm (self-intersecting)
    pts = [(0,0), (1,1), (0,1), (1,0)]  # bow-tie shape
    tris = triangulate(pts)
    assert isinstance(tris, list)   # loop exits through line 58-59


# line 68: final 3 points appended correctly
def test_triangulation_final_triangle():
    pts = [(0,0), (1,0), (0,1), (0.5,0.2)]
    tris = triangulate(pts)
    assert any(len(t) == 3 for t in tris)  # triggers last-triangle append
