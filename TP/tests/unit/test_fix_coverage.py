import pytest
import struct
from unittest.mock import patch

from TP.triangulator.binary import decode_triangles
from TP.triangulator.server import app
from TP.triangulator.triangulation import triangulate
from TP.pointset import PointSet


# =======================================================
# 1) يغطي binary.py الأسطر 59 و 65
# =======================================================

def test_decode_triangles_no_triangle_section():
    # Point count = 1 + point (1.0, 2.0)
    # بدون قسم المثلثات
    data = struct.pack(">Iff", 1, 1.0, 2.0)

    ps, tris = decode_triangles(data)

    assert isinstance(ps, PointSet)
    assert ps.points == [(1.0, 2.0)]
    assert tris == []  # يغطي السطرين 59 و 65


# =======================================================
# 2) يغطي server.py السطر 45
# =======================================================

def test_server_exception_502():
    from TP.triangulator import server as srv

    class FakeClient:
        def get_pointset(self, *_):
            raise Exception("forced crash")  # يمر مباشرة إلى except

    with patch.object(srv, "client", FakeClient()):
        cl = app.test_client()
        r = cl.get("/triangulate/123")
        assert r.status_code == 502  # ← يغطي السطر 45 بالكامل


# =======================================================
# 3) يغطي triangulation.py السطر 28 (points < 3)
# =======================================================

def test_triangulate_not_enough_points():
    result = triangulate([(0, 0), (1, 1)])
    assert result == []  # يغطي السطر 28


# =======================================================
# 4) يغطي triangulation.py السطر 68 (آخر مثلث)
# =======================================================

def test_triangulate_final_triangle_executed():
    pts = [(0, 0), (1, 0), (1, 1), (0, 1)]
    tris = triangulate(pts)

    # يجب أن تنتهي بتثبيت آخر مثلث في السطر 68
    assert any(len(t) == 3 for t in tris)
