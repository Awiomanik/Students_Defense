import hypothesis.strategies as st
from hypothesis import given
import pytest
from functions_from_utilities import Coord

def grid_middle_point(coords : 'Coord', tile_size : int = 120) -> 'Coord':
        """Takes grid position and return pixel position of middle point in tile."""
        return Coord(coords.x*tile_size + tile_size//2, coords.y*tile_size + tile_size//2)

@given(st.integers(), st.integers(), st.integers(min_value=1))
def test_grid_middle_point(x, y, tile_size):
    coord = Coord(x, y)
    result = grid_middle_point(coord, tile_size)
    assert result == Coord(coord.x*tile_size + tile_size//2, coord.y*tile_size + tile_size//2)

if __name__ == '__main__':
    pytest.main()
