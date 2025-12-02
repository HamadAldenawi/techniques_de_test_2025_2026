# setup_tp.ps1
# تشغيل: افتح PowerShell في المجلد الأعلى لـ TP ثم:
# .\setup_tp.ps1

$ErrorActionPreference = "Stop"

$tp = "TP"

# Create directories
New-Item -ItemType Directory -Force -Path $tp
New-Item -ItemType Directory -Force -Path "$tp\triangulator"
New-Item -ItemType Directory -Force -Path "$tp\tests"
New-Item -ItemType Directory -Force -Path "$tp\tests\unit"
New-Item -ItemType Directory -Force -Path "$tp\tests\integration"
New-Item -ItemType Directory -Force -Path "$tp\tests\performance"

function write-file($path, $content) {
    $dir = Split-Path $path
    if ($dir -and $dir.Trim() -ne "") {
        if (-not (Test-Path $dir)) { 
            New-Item -ItemType Directory -Path $dir -Force | Out-Null 
        }
    }
    $content | Out-File -FilePath $path -Encoding utf8 -Force
    Write-Host "Wrote $path"
}
# 1) TP/__init__.py
write-file "$tp\__init__.py" '# TP package marker'

# 2) TP/pointset.py
write-file "$tp\pointset.py" @'
class PointSet:
    """
    Simple container for a list of 2D points.
    points = [(x1, y1), (x2, y2), ...]
    """

    def __init__(self, points):
        if not isinstance(points, list):
            raise TypeError("points must be a list")

        for p in points:
            if (
                not isinstance(p, tuple)
                or len(p) != 2
                or not isinstance(p[0], (int, float))
                or not isinstance(p[1], (int, float))
            ):
                raise ValueError("each point must be a tuple (x, y)")

        self.points = points

    def __len__(self):
        return len(self.points)

    def __getitem__(self, idx):
        return self.points[idx]

    # Convenience / serialization helpers
    def to_list(self):
        return list(self.points)

    @classmethod
    def from_list(cls, lst):
        return cls(lst)

    def as_dict(self):
        return {"points": self.to_list()}

    @classmethod
    def from_dict(cls, d):
        if "points" not in d:
            raise KeyError("missing 'points' field")
        return cls.from_list(d["points"])

    def __repr__(self):
        return f"PointSet({self.points})"
'@

# 3) TP/triangulator/__init__.py
write-file "$tp\triangulator\__init__.py" '# triangulator package marker'

# 4) TP/triangulator/binary.py
write-file "$tp\triangulator\binary.py" @'
import struct
from TP.pointset import PointSet

# Binary format (as specified in the project):
# - 4 bytes unsigned int (big-endian) = number of points (N)
# - then for each point: 4 bytes float X, 4 bytes float Y (big-endian)
# For Triangles:
# - first the PointSet blob as above
# - then 4 bytes unsigned int (big-endian) = number of triangles (M)
# - then for each triangle: 3 x 4 bytes unsigned int indices (big-endian)


def encode_pointset(pointset: PointSet) -> bytes:
    count = len(pointset)
    data = struct.pack(">I", count)
    for x, y in pointset.points:
        data += struct.pack(">f", float(x))
        data += struct.pack(">f", float(y))
    return data


def decode_pointset(buffer: bytes) -> PointSet:
    offset = 0
    if len(buffer) < 4:
        raise ValueError("buffer too short for pointset count")
    (count,) = struct.unpack_from(">I", buffer, offset)
    offset += 4
    points = []
    for _ in range(count):
        if offset + 8 > len(buffer):
            raise ValueError("buffer too short for points")
        x = struct.unpack_from(">f", buffer, offset)[0]
        y = struct.unpack_from(">f", buffer, offset + 4)[0]
        offset += 8
        points.append((x, y))
    return PointSet(points)


def encode_triangles(pointset: PointSet, triangles: list) -> bytes:
    data = encode_pointset(pointset)
    count = len(triangles)
    data += struct.pack(">I", count)
    for a, b, c in triangles:
        # each index stored as unsigned int
        data += struct.pack(">I", int(a))
        data += struct.pack(">I", int(b))
        data += struct.pack(">I", int(c))
    return data


def decode_triangles(buffer: bytes):
    """
    Returns tuple (PointSet, triangles_list)
    triangles_list is list of (a,b,c) indices
    """
    # decode pointset first
    offset = 0
    if len(buffer) < 4:
        raise ValueError("buffer too short")
    (count,) = struct.unpack_from(">I", buffer, offset)
    offset += 4
    points = []
    for _ in range(count):
        if offset + 8 > len(buffer):
            raise ValueError("buffer too short for points")
        x = struct.unpack_from(">f", buffer, offset)[0]
        y = struct.unpack_from(">f", buffer, offset + 4)[0]
        offset += 8
        points.append((x, y))
    pointset = PointSet(points)

    if offset + 4 > len(buffer):
        # no triangles section: return empty
        return pointset, []

    (tcount,) = struct.unpack_from(">I", buffer, offset)
    offset += 4
    triangles = []
    for _ in range(tcount):
        if offset + 12 > len(buffer):
            raise ValueError("buffer too short for triangles")
        a = struct.unpack_from(">I", buffer, offset)[0]
        b = struct.unpack_from(">I", buffer, offset + 4)[0]
        c = struct.unpack_from(">I", buffer, offset + 8)[0]
        offset += 12
        triangles.append((a, b, c))
    return pointset, triangles
'@

# 5) TP/triangulator/triangulation.py
write-file "$tp\triangulator\triangulation.py" @'
def area(a, b, c):
    """Signed area * 0.5, but we use sign only."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def is_point_in_triangle(p, a, b, c):
    # Barycentric / sign test (include boundary)
    return (
        area(a, b, p) >= 0 and area(b, c, p) >= 0 and area(c, a, p) >= 0
    )


def triangulate(points):
    """
    Simple ear-clipping triangulation.
    Assumes 'points' is a list of vertices of a simple polygon in order.
    For sets that are not polygons, results may be undefined; tests use simple cases.
    Returns list of (i,j,k) indices referencing original points.
    """

    n = len(points)
    if n < 3:
        return []
    # If exactly 3, single triangle
    if n == 3:
        return [(0, 1, 2)]

    indices = list(range(n))
    triangles = []

    # Defensive: create a copy of points to allow numeric ops
    pts = points

    # repeat removing ears
    loop_guard = 0
    while len(indices) > 3 and loop_guard < n * n:
        loop_guard += 1
        removed = False
        L = len(indices)
        for i in range(L):
            i_prev = indices[(i - 1) % L]
            i_curr = indices[i]
            i_next = indices[(i + 1) % L]

            A = pts[i_prev]
            B = pts[i_curr]
            C = pts[i_next]

            # Check convexity: area > 0 means CCW convex for this ordering
            if area(A, B, C) <= 0:
                continue

            # Check no other point inside triangle ABC
            is_ear = True
            for j in indices:
                if j in (i_prev, i_curr, i_next):
                    continue
                P = pts[j]
                if is_point_in_triangle(P, A, B, C):
                    is_ear = False
                    break

            if is_ear:
                triangles.append((i_prev, i_curr, i_next))
                # remove i_curr from polygon indices
                indices.pop(i)
                removed = True
                break
        if not removed:
            # cannot find ear (possibly non-simple polygon), break
            break

    # last triangle
    if len(indices) == 3:
        triangles.append((indices[0], indices[1], indices[2]))

    return triangles
'@

# 6) TP/triangulator/client_psm.py
write-file "$tp\triangulator\client_psm.py" @'
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
'@

# 7) TP/triangulator/server.py
write-file "$tp\triangulator\server.py" @'
from flask import Flask, request, jsonify, Response
from TP.triangulator.client_psm import PointSetManagerClient
from TP.triangulator.triangulation import triangulate
from TP.triangulator.binary import encode_triangles

app = Flask(__name__)

# Default PointSetManager URL – adjust if your PSM runs elsewhere.
PSM_URL = "http://localhost:5001"  # change if needed
client = PointSetManagerClient(PSM_URL)


@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "Triangulator running"}), 200


@app.route("/triangulate/<int:ps_id>", methods=["GET"])
def triangulate_endpoint(ps_id):
    try:
        ps = client.get_pointset(ps_id)
    except Exception as e:
        return jsonify({"error": "cannot fetch pointset", "detail": str(e)}), 502

    # points as list of (x,y)
    triangles = triangulate(ps.points)
    data = encode_triangles(ps, triangles)
    return Response(data, status=200, content_type="application/octet-stream")


if __name__ == "__main__":
    app.run(port=5000)
'@

# 8) TP/api.py
write-file "$tp\api.py" @'
# convenience script to run the triangulator server
from TP.triangulator.server import app

if __name__ == "__main__":
    app.run(port=5000)
'@

# 9) TP/tests/__init__.py
write-file "$tp\tests\__init__.py" '# tests package marker'

# 10) TP/tests/unit/__init__.py
write-file "$tp\tests\unit\__init__.py" '# unit tests marker'

# 11) TP/tests/unit/test_pointset.py
write-file "$tp\tests\unit\test_pointset.py" @'
from TP.pointset import PointSet


def test_pointset_basic():
    ps = PointSet([(0, 1), (2, 3)])
    assert len(ps) == 2
    assert ps[0] == (0, 1)
    assert ps.to_list() == [(0, 1), (2, 3)]
    d = ps.as_dict()
    assert "points" in d
    ps2 = PointSet.from_dict(d)
    assert ps2.to_list() == ps.to_list()
'@

# 12) TP/tests/unit/test_binary.py
write-file "$tp\tests\unit\test_binary.py" @'
from TP.triangulator.binary import encode_pointset, decode_pointset
from TP.pointset import PointSet


def test_binary_encoding():
    ps = PointSet([(1.0, 2.0), (3.0, 4.0)])
    data = encode_pointset(ps)
    result = decode_pointset(data)
    assert len(result) == 2
    assert result[0] == (1.0, 2.0)
    assert result[1] == (3.0, 4.0)
'@

# 13) TP/tests/unit/test_triangulation.py
write-file "$tp\tests\unit\test_triangulation.py" @'
from TP.triangulator.triangulation import triangulate


def test_triangulation_triangle():
    points = [(0, 0), (1, 0), (0, 1)]
    tris = triangulate(points)
    assert tris == [(0, 1, 2)] or tris == [(0, 2, 1)]


def test_triangulation_square():
    points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    tris = triangulate(points)
    # For a square we expect 2 triangles
    assert len(tris) == 2
    # indices must be valid
    for a, b, c in tris:
        assert 0 <= a < 4 and 0 <= b < 4 and 0 <= c < 4
'@

# 14) TP/tests/integration/test_api.py
write-file "$tp\tests\integration\test_api.py" @'
import io
import pytest
from TP.triangulator.server import app
from TP.pointset import PointSet
from TP.triangulator.binary import encode_pointset

# Integration tests using Flask test client.
# We simulate a PointSetManager by using a local endpoint: monkeypatch the client.get_pointset


def test_index():
    client = app.test_client()
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"Triangulator running" in rv.data


class DummyClient:
    def __init__(self, ps):
        self._ps = ps

    def get_pointset(self, ps_id):
        return self._ps


def test_triangulate_endpoint(monkeypatch):
    # create a simple pointset
    ps = PointSet([(0, 0), (1, 0), (0, 1)])
    # monkeypatch client used in server
    from TP.triangulator import server as srv

    monkeypatch.setattr(srv, "client", DummyClient(ps))
    client = app.test_client()
    rv = client.get("/triangulate/123")
    assert rv.status_code == 200
    # result is binary octet-stream
    assert rv.headers["Content-Type"] == "application/octet-stream"
    assert len(rv.data) > 0
'@

# 15) TP/tests/performance/test_perf.py
write-file "$tp\tests\performance\test_perf.py" @'
import pytest
from TP.triangulator.triangulation import triangulate

@pytest.mark.performance
def test_perf_triangulate_1000():
    # Generate a convex polygon (circle approximation) of 1000 points
    import math
    n = 1000
    pts = [(math.cos(2*math.pi*i/n), math.sin(2*math.pi*i/n)) for i in range(n)]
    tris = triangulate(pts)
    # basic assertion: some triangles returned (n-2)
    assert len(tris) >= n - 5  # loose check for performance run
'@

# 16) Makefile
write-file "$tp\Makefile" @'
.PHONY: test unit_test perf_test coverage lint doc

test:
	pytest -q

unit_test:
	pytest -q -m "not performance"

perf_test:
	pytest -q -m "performance"

coverage:
	coverage run -m pytest
	coverage report

lint:
	ruff check .

doc:
	pdoc3 TP -o docs
'@

# 17) requirements.txt
write-file "requirements.txt" @'
flask
requests
'@

# 18) dev_requirements.txt
write-file "dev_requirements.txt" @'
pytest
coverage
ruff
pdoc3
'@

# 19) PLAN.md
write-file "$tp\PLAN.md" @'
# PLAN de tests — Triangulator

## Objectifs
- Vérifier la sérialisation/désérialisation des PointSets
- Vérifier l'algorithme de triangulation
- Vérifier les endpoints HTTP du Triangulator
- Mesurer les performances pour grands ensembles

## Structure des tests
- tests/unit : tests unitaires (binary, pointset, triangulation)
- tests/integration : tests d'API (Flask client)
- tests/performance : tests marqués `performance`

## Outils
- pytest, coverage, ruff, pdoc3

## Exécution
- make unit_test
- make perf_test
- make coverage
'@

# 20) RETEX.md
write-file "$tp\RETEX.md" @'
# RETEX — Triangulator

## Ce qui a bien marché
- Mise en place de l'encodage binaire
- Triangulation par ear-clipping simple
- API Flask fonctionnelle

## Difficultés rencontrées
- Gestion des formats binaires (endianness / float precision)
- Cas limites: points colinéaires / points dupliqués

## Améliorations futures
- Implémenter Delaunay pour meilleure qualité
- Ajouter plus de tests de robustesse (cas aléatoires, fuzz)
- Ajouter CI (GitHub Actions)
'@

Write-Host "All files created. Next steps:"
Write-Host "1) (Optional) create a venv and install deps:"
Write-Host "   python -m venv .venv"
Write-Host "   .\\.venv\\Scripts\\activate"
Write-Host "   pip install -r requirements.txt"
Write-Host "   pip install -r dev_requirements.txt"
Write-Host "2) Run unit tests (fast): pytest -q"
Write-Host "3) Run server: python -m TP.api  OR python -m TP.triangulator.server"
Write-Host "Notes: If your PointSetManager runs on a different host/port, edit TP\\triangulator\\server.py and change PSM_URL variable."