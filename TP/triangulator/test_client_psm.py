from TP.triangulator.client_psm import PointSetManagerClient
from TP.pointset import PointSet
from TP.triangulator.binary import encode_pointset
from unittest.mock import patch, MagicMock

def test_client_success():
    client = PointSetManagerClient("http://fake")

    # PointSet expected
    ps = PointSet([(1, 2), (3, 4)])
    encoded = encode_pointset(ps)   # ← binary format الصحيح

    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.content = encoded  # ← لازم يكون bytes

    with patch("requests.get", return_value=fake_response):
        result = client.get_pointset(1)

    assert isinstance(result, PointSet)
    assert result.points == [(1, 2), (3, 4)]
