import pytest
from unittest.mock import patch, MagicMock

from TP.pointset import PointSet
from TP.triangulator.binary import decode_pointset, decode_triangles, encode_pointset
from TP.triangulator.client_psm import PointSetManagerClient
from TP.triangulator.server import app
from TP.triangulator import server as srv


# ---------------------------------------------------------
# 1) تغطية binary.py (الأسطر الغير مغطاة)
# ---------------------------------------------------------

def test_decode_pointset_header_too_small():
    with pytest.raises(ValueError):
        decode_pointset(b"\x00")


def test_decode_triangles_without_triangle_section():
    ps = PointSet([(1, 2)])
    encoded = encode_pointset(ps)
    decoded_ps, triangles = decode_triangles(encoded)
    assert decoded_ps.points == [(1, 2)]
    assert triangles == []


# ---------------------------------------------------------
# 2) تغطية client_psm.py (حالة binary غير صحيح)
# ---------------------------------------------------------

def test_client_psm_invalid_binary():
    client = PointSetManagerClient("http://fake")

    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.content = b""  # ليس binary صالح

    with patch("requests.get", return_value=fake_response):
        with pytest.raises(ValueError):
            client.get_pointset(1)


# ---------------------------------------------------------
# 3) تغطية server.py (except block)
# ---------------------------------------------------------

def test_server_exception_block(monkeypatch):
    class FakeBadClient:
        def get_pointset(self, ps_id):
            raise Exception("BOOM")

    monkeypatch.setattr(srv, "client", FakeBadClient())

    client = app.test_client()
    rv = client.get("/triangulate/5")

    assert rv.status_code == 502
    assert b"cannot fetch pointset" in rv.data
