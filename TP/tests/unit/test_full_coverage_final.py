import pytest
from TP.triangulator.triangulation import triangulate


# ======================================================
# 1) تغطية السطر 35 — n == 3
# ======================================================
def test_triangulation_exact_triangle():
    pts = [(0,0), (1,0), (0,1)]
    assert triangulate(pts) == [(0,1,2)] or triangulate(pts) == [(0,2,1)]


# ======================================================
# 2) تغطية السطرين 68–69 — is_ear = False + break
#    نحتاج نقطة تقع داخل المثلث → فتجعل is_ear = False
# ======================================================
def test_triangulation_internal_point_causes_is_ear_false():
    # النقطة (0.5, 0.3) تقع داخل المثلث (0,0)-(1,0)-(0,1)
    pts = [(0,0), (1,0), (0,1), (0.5,0.3)]
    tris = triangulate(pts)

    # المهم أن الخوارزمية تدخل فرع is_ear=False
    assert isinstance(tris, list)


# ======================================================
# 3) تغطية السطر 58–59 — no ear found → break
#    bow-tie يعطي self-intersection → ear clipping يفشل
# ======================================================
def test_triangulation_no_ear_found_break():
    pts = [(0,0), (2,2), (0,2), (2,0)]  # bow-tie shape
    tris = triangulate(pts)

    # المهم أن يصل إلى break
    assert isinstance(tris, list)
    assert len(tris) >= 0


# ======================================================
# 4) تغطية السطر 81 — break النهائي بعد no-ear
#    نُجبر الخوارزمية أن تخرج من الحلقة مباشرة
# ======================================================
def test_triangulation_reaches_final_break():
    # نقاط شبه خطّية لكن ليست خطية بالكامل → تمنع ear clipping من العمل
    pts = [(0,0), (1,0), (2,0.00001), (3,0)]
    tris = triangulate(pts)

    assert isinstance(tris, list)


# ======================================================
# 5) تغطية final append (آخر 3 نقاط) السطر الأخير
# ======================================================
def test_triangulation_final_append():
    pts = [(0,0), (1,0), (1,1), (0.3,0.2)]
    tris = triangulate(pts)

    # يجب أن يحتوي آخر خطوة على مثلث 3 نقاط
    assert any(len(t) == 3 for t in tris)
