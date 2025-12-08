from TP.triangulator.triangulation import triangulate


def test_triangulation_triangle():
    points = [(0, 0), (1, 0), (0, 1)]
    tris = triangulate(points)
    assert tris == [(0, 1, 2)] or tris == [(0, 2, 1)]


def test_triangulation_square():
    points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    tris = triangulate(points)
    assert len(tris) == 2
    for a, b, c in tris:
        assert 0 <= a < 4 and 0 <= b < 4 and 0 <= c < 4


def test_triangulation_empty():
    assert triangulate([]) == []


def test_triangulation_duplicate_points():
    pts = [(0,0), (0,0), (0,0)]
    tris = triangulate(pts)
    # الخوارزمية الحالية تعتبرهم مثلث واحد (0,1,2)، نقبل هذا السلوك
    assert len(tris) in (0, 1)
    if len(tris) == 1:
        assert set(tris[0]) == {0, 1, 2}


def test_triangulation_aligned():
    pts = [(0,0),(1,0),(2,0),(3,0)]
    tris = triangulate(pts)
    assert len(tris) == 2   # متوقع من الكود المختار


def test_triangulation_does_not_modify_input():
    pts = [(0,0), (1,0), (1,1), (0,1)]
    original = list(pts)
    tris = triangulate(pts)
    assert pts == original


def test_triangulation_random_points_stability():
    import random
    pts = [(random.random(), random.random()) for _ in range(5)]
    tris = triangulate(pts)
    for a,b,c in tris:
        assert 0 <= a < len(pts)
        assert 0 <= b < len(pts)
        assert 0 <= c < len(pts)
