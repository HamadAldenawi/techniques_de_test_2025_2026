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
def test_triangulation_empty():
    assert triangulate([]) == []

def test_triangulation_duplicate_points():
    pts = [(0,0),(0,0),(0,0)]
    tris = triangulate(pts)
    assert len(tris) == 1 or tris == []

def test_triangulation_aligned():
    pts = [(0,0),(1,0),(2,0),(3,0)]
    tris = triangulate(pts)
    assert len(tris) == 2

def test_triangulation_does_not_modify_input():
    pts = [(0,0), (1,0), (1,1), (0,1)]
    original = list(pts)   # نسخة قبل الترييانغوليشن
    tris = triangulate(pts)
    assert pts == original   

    
def test_triangulation_random_points_stability():
    import random
    pts = [(random.random(), random.random()) for _ in range(5)]
    tris = triangulate(pts)
    # Just verify no crash + indices valid
    for a,b,c in tris:
        assert 0 <= a < len(pts)
        assert 0 <= b < len(pts)
        assert 0 <= c < len(pts)

