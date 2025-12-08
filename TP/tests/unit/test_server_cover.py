from TP.triangulator.server import app
from unittest.mock import patch

def test_server_unexpected_exception():
    client = app.test_client()

    with patch("TP.triangulator.server.client.get_pointset",
               side_effect=Exception("boom")):
        rv = client.get("/triangulate/1")
        assert rv.status_code == 502
def test_server_internal_exception():
    with patch("TP.triangulator.server.client.get_pointset", side_effect=Exception("boom")):
        client = app.test_client()
        rv = client.get("/triangulate/1")
        assert rv.status_code == 502

        