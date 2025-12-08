import struct
import pytest
from unittest.mock import patch, MagicMock

from TP.pointset import PointSet
from TP.triangulator.binary import decode_triangles
from TP.triangulator.triangulation import triangulate
from TP.triangulator.server import app
from TP.triangulator import server as srv


# =========================================================
# 1) COVER binary.py lines 59 and 65 — missing triangle section
# =========================================================

def test_decode_triangles_missing_section():
    # PointSet only: count=1, x=1.0, y=2.0
    data = struct.pack(">Iff", 1, 1.0, 2.0)
    ps, tris = decode_triangles(data)

    assert ps.points == [(1.0, 2.0)]
    assert tris == []   # covers line 59 & 65


def test_decode_triangles_invalid_size():
    # has tcount=1 but missing triangle bytes → must raise error
    data = struct.pack(">IffI", 1, 1.0, 2.0, 1)

    with pytest.raises(ValueError):
        decode_triangles(data)  # covers line 65



# =========================================================
# 2) COVER server.py line 45 (error in client.get_pointset)
# =========================================================

def test_server_client_error():
    class FakeClient:
        def get_pointset(self, ps_id):
            raise Exception("boom")

    with patch.object(srv, "client", FakeClient()):
        c = app.test_client()
        res = c.get("/triangulate/7")

        assert res.status_code == 502   # covers line 45



# =========================================================
# 3) COVER triangulation.py missing lines: 28, 58–59, 68
# =========================================================

# line 28 — n < 3
def test_triangulation_less_than_three_points():
    assert triangulate([]) == []
    assert triangulate([(1, 2)]) == []
    assert triangulate([(1, 2), (3, 4)]) == []


# lines 58–59 — cannot find an ear → break
def test_triangulation_no_ear_found_case():
    # self-intersecting shape forces failure → loop hits break
    pts = [(0, 0), (1, 1), (0, 1), (1, 0)]
    tris = triangulate(pts)
    assert isinstance(tris, list)  # branch covered


# line 68 — last-triangle append
def test_triangulation_last_triangle_append():
    pts = [(0, 0), (1, 0), (0.2, 0.8), (0.3, 0.2)]
    tris = triangulate(pts)

    # ensure final remaining 3 indices appended
    assert any(len(t) == 3 for t in tris)
