import pytest
from TP.pointset import PointSet


def test_pointset_invalid_constructor_type():
    # الكود يرفع TypeError وليس ValueError
    with pytest.raises(TypeError):
        PointSet("not a list")


def test_pointset_invalid_point_structure():
    # الكود يرفع ValueError لأن العناصر ليست tuples
    with pytest.raises(ValueError):
        PointSet.from_list([1, 2, 3])


def test_pointset_from_dict_missing_key():
    # الكود يرفع KeyError عند غياب المفتاح points
    with pytest.raises(KeyError):
        PointSet.from_dict({})

def test_pointset_repr():
    ps = PointSet([(1,2)])
    r = repr(ps)
    assert "PointSet" in r
    assert "(1, 2)" in r