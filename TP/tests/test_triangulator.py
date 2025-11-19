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
