import pytest
from TP.triangulator.triangulation import triangulate

@pytest.mark.performance
def test_perf_triangulate_1000():
    import math
    n = 1000
    pts = [(math.cos(2*math.pi*i/n), math.sin(2*math.pi*i/n)) for i in range(n)]
    tris = triangulate(pts)
    assert len(tris) >= n - 5
