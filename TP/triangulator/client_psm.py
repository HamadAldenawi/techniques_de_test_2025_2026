import requests
from TP.triangulator.binary import decode_pointset
from TP.pointset import PointSet

# Simple client to retrieve PointSet binary from a PointSetManager
# Expected endpoint: GET http://<host>:<port>/pointset/<id>
# Returns PointSet instance or raises exception on error


class PointSetManagerClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get_pointset(self, ps_id: int) -> PointSet:
        url = f"{self.base_url}/pointset/{ps_id}"
        resp = requests.get(url)
        if resp.status_code != 200:
            raise RuntimeError(f"PointSetManager returned {resp.status_code}")
        # body is binary PointSet format
        return decode_pointset(resp.content)
