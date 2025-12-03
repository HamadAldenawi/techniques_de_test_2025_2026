import io
import pytest
from TP.triangulator.server import app
from TP.pointset import PointSet
from TP.triangulator.binary import encode_pointset

# ----------------------------------------------------------
# 1) TEST: / returns healthy message
# ----------------------------------------------------------

def test_index():
    client = app.test_client()
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"Triangulator running" in rv.data


# ----------------------------------------------------------
# Dummy PointSetManager client for integration test
# ----------------------------------------------------------

class DummyClient:
    def __init__(self, ps):
        self._ps = ps

    def get_pointset(self, ps_id):
        return self._ps


# ----------------------------------------------------------
# 2) TEST triangulate/<id> with monkeypatch
# ----------------------------------------------------------

def test_triangulate_endpoint(monkeypatch):
    ps = PointSet([(0, 0), (1, 0), (0, 1)])

    from TP.triangulator import server as srv
    monkeypatch.setattr(srv, "client", DummyClient(ps))

    client = app.test_client()
    rv = client.get("/triangulate/123")

    assert rv.status_code == 200
    assert rv.headers["Content-Type"] == "application/octet-stream"
    assert len(rv.data) > 0


# ----------------------------------------------------------
# 3) TEST PointSetManager 404 (ID inexistant)
# ----------------------------------------------------------

def test_psm_missing_id(monkeypatch):
    from TP.triangulator import server as srv

    class FakeClient404:
        def get_pointset(self, ps_id):
            return None

    monkeypatch.setattr(srv, "client", FakeClient404())

    client = app.test_client()
    rv = client.get("/triangulate/9999")

    assert rv.status_code == 502


# ----------------------------------------------------------
# 4) TEST malformed JSON to PointSetManager (simulation)
# ----------------------------------------------------------

def test_psm_invalid_json(monkeypatch):
    from TP.triangulator import server as srv

    class FakeBadClient:
        def get_pointset(self, ps_id):
            raise ValueError("invalid json")

    monkeypatch.setattr(srv, "client", FakeBadClient())

    client = app.test_client()
    rv = client.get("/triangulate/10")

    assert rv.status_code == 502


# ----------------------------------------------------------
# 5) TEST missing triangulation ID in triangulator
# ----------------------------------------------------------

def test_triangulator_missing_id(monkeypatch):
    from TP.triangulator import server as srv

    class FakeNoneClient:
        def get_pointset(self, ps_id):
            return None

    monkeypatch.setattr(srv, "client", FakeNoneClient())

    client = app.test_client()
    rv = client.get("/triangulate/99999")

    assert rv.status_code == 502


# ----------------------------------------------------------
# EXTRA TEST 1 – Test valid JSON structure from "/" endpoint
# ----------------------------------------------------------

def test_api_root_json_format():
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, dict)
    assert "status" in data


# ----------------------------------------------------------
# EXTRA TEST 2 – Test empty PointSet triangulation
# ----------------------------------------------------------

def test_triangulate_empty_pointset(monkeypatch):
    from TP.triangulator import server as srv

    class FakeEmptyPS:
        def get_pointset(self, ps_id):
            return PointSet([])

    monkeypatch.setattr(srv, "client", FakeEmptyPS())

    client = app.test_client()
    res = client.get("/triangulate/1")

    assert res.status_code == 200
    assert res.headers["Content-Type"] == "application/octet-stream"
    assert len(res.data) > 0  # binary format is valid even if empty


# ----------------------------------------------------------
# EXTRA TEST 3 – Internal crash → must return 502
# ----------------------------------------------------------

def test_api_internal_error(monkeypatch):
    from TP.triangulator import server as srv

    class FakeCrash:
        def get_pointset(self, ps_id):
            raise RuntimeError("unexpected")

    monkeypatch.setattr(srv, "client", FakeCrash())

    client = app.test_client()
    res = client.get("/triangulate/55")

    assert res.status_code == 502
