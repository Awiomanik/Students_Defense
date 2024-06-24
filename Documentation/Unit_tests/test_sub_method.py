import hypothesis.strategies as st
from hypothesis import given
import pytest
from functions_from_utilities import Coord

@given(st.integers(), st.integers(), st.integers(), st.integers())
def test_sub_two_coords(x1, y1, x2, y2):
    coord1 = Coord(x1, y1)
    coord2 = Coord(x2, y2)
    result = coord1 - coord2
    assert result == Coord(x1 - x2, y1 - y2)

@given(st.integers(), st.integers(), st.integers())
def test_sub_coord_and_int(x, y, num_int):
    coord = Coord(x, y)
    result = coord - num_int
    assert result == Coord(x - num_int, y - num_int)

@given(st.integers(), st.integers(), st.floats(allow_nan=False))
def test_add_coord_and_float(x, y, num_float):
    coord = Coord(x, y)
    result = coord - num_float
    assert result == Coord(x - num_float, y - num_float)

def test_add_invalid_type():
    coord = Coord(1, 2)
    with pytest.raises(NotImplementedError):
        coord + "string"

if __name__ == '__main__':
    pytest.main()