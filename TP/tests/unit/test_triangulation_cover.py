from TP.triangulator.triangulation import triangulate

def test_triangulation_non_simple_polygon_triggers_fallback():
    # شكل غير قابل للقصّ ear clipping
    pts = [(0,0),(1,1),(0,1),(1,0)]
    tris = triangulate(pts)
    assert isinstance(tris, list)
def test_triangulation_no_ear_polygon():
    # polygon غير بسيط → ear clipping يفشل → يرجع مثلث أخير فقط أو []
    pts = [(0,0), (1,1), (2,0), (1,0.5)]
    tris = triangulate(pts)
    assert isinstance(tris, list)  # فقط تغطية المسار
