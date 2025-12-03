import pytest
import time
from TP.triangulator.triangulation import triangulate


@pytest.mark.performance
def test_perf_triangulate_1000():
    import math
    n = 1000
    pts = [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n)]
    tris = triangulate(pts)
    assert len(tris) >= n - 5   # tolérance faible


# ------------------------------------------------------
# TEST 2 : performance sur un grand ensemble (2000 points)
# ------------------------------------------------------
@pytest.mark.performance
def test_perf_triangulate_2000():
    import math
    n = 2000
    pts = [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n)]

    tris = triangulate(pts)

    # on vérifie que le résultat contient un nombre raisonnable de triangles
    assert len(tris) >= n - 10   # marge tolérable


# ------------------------------------------------------
# TEST 3 : triangulation doit s'exécuter en < 1 seconde
# ------------------------------------------------------
@pytest.mark.performance
def test_perf_triangulate_under_3s():
    import math
    n = 1500
    pts = [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n)]

    start = time.time()
    _ = triangulate(pts)
    duration = time.time() - start

    # performance acceptable pour un PC normal
    assert duration < 3.0
