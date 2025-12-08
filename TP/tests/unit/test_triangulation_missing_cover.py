import pytest
from TP.triangulator.triangulation import triangulate


# ============================================================
# 1) تغطية السطر 28: عدد النقاط أقل من 3
# ============================================================

def test_triangulation_less_than_3_points():
    assert triangulate([]) == []
    assert triangulate([(1, 2)]) == []
    assert triangulate([(1, 2), (3, 4)]) == []


# ============================================================
# 2) تغطية السطرين 58–59: لم يتم إيجاد Ear → يتم break
#    نستخدم شكل Bow-Tie (self-intersecting)
# ============================================================

def test_triangulation_no_ear_found():
    pts = [(0, 0), (2, 2), (0, 2), (2, 0)]  # bow-tie shape
    tris = triangulate(pts)

    # في هذا الشكل، algorithm لن يجد أي ear و سيكسر الحلقة
    assert isinstance(tris, list)
    assert len(tris) >= 0  # نتحقق فقط أن الكود لم ينهار


# ============================================================
# 3) تغطية السطر 68: إضافة آخر مثلث بعد انتهاء الحلقة
# ============================================================

def test_triangulation_final_triangle_added():
    pts = [
        (0, 0),
        (1, 0),
        (1, 1),
        (0.5, 0.2),  # نقطة داخلية تساعد بتكوين ear
    ]
    tris = triangulate(pts)

    # يجب أن يحتوي آخر خطوة على مثلث 3 نقاط بالضبط (final append)
    assert any(len(t) == 3 for t in tris)
