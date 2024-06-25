import hypothesis.strategies as st
from hypothesis import given
import pytest
from functions_from_utilities import Coord

@given(st.integers(), st.integers(), st.integers(), st.integers())
def test_add_two_coords(x1, y1, x2, y2):
    coord1 = Coord(x1, y1)
    coord2 = Coord(x2, y2)
    result = coord1 + coord2
    assert result == Coord(x1 + x2, y1 + y2)

@given(st.integers(), st.integers(), st.integers())
def test_add_coord_and_int(x, y, num_int):
    coord = Coord(x, y)
    result = coord + num_int
    assert result == Coord(x + num_int, y + num_int)

@given(st.integers(), st.integers(), st.floats(allow_nan=False))
def test_add_coord_and_float(x, y, num_float):
    coord = Coord(x, y)
    result = coord + num_float
    assert result == Coord(x + num_float, y + num_float)

def test_add_invalid_type():
    coord = Coord(1, 2)
    with pytest.raises(NotImplementedError):
        coord + "string"

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

@given(st.integers(), st.integers())
def test_repr_of_coord(x, y):
    coord = Coord(x, y)
    result = repr(coord)
    assert result == f"x.{x}, y.{y}"


@given(st.integers(), st.integers())
def test_iter(x, y):
        coord = Coord(x,y)
        iter_values = list(coord)
        assert iter_values == [x, y]

def res2tile(coords : tuple[int, int], tile_size : int = 120) -> 'Coord':
        return Coord(coords[0] // tile_size, coords[1] // tile_size)

@given(st.tuples(st.integers(), st.integers()), st.integers(min_value=1))
def test_res2tile(coord, tile_size):
    result = res2tile(coord, tile_size)
    assert result ==  Coord((coord[0] // tile_size, coord[1] // tile_size))


def grid_middle_point(coords : 'Coord', tile_size : int = 120) -> 'Coord':
        """Takes grid position and return pixel position of middle point in tile."""
        return Coord(coords.x*tile_size + tile_size//2, coords.y*tile_size + tile_size//2)

@given(st.integers(), st.integers())
def test_grid_middle_point(x, y, tile_size):
    coord = Coord(x, y)
    result = grid_middle_point(coord, tile_size)
    assert result ==  Coord(x*tile_size + tile_size//2, y*tile_size + tile_size//2)


if __name__ == '__main__':
    pytest.main()
