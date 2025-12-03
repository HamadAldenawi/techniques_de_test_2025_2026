import pytest
from unittest.mock import patch
from TP.triangulator.client_psm import PointSetManagerClient

def test_client_psm_network_error():
    client = PointSetManagerClient("http://fake")

    with patch("requests.get", side_effect=Exception("network down")):
        with pytest.raises(Exception):
            client.get_pointset(5)
            