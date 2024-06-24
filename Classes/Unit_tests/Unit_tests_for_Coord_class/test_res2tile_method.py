import hypothesis.strategies as st
from hypothesis import given
import pytest
from functions_from_utilities import Coord

def res2tile(coords : tuple[int, int], tile_size : int = 120) -> 'Coord':
        return Coord(coords[0] // tile_size, coords[1] // tile_size)

@given(st.tuples(st.integers(), st.integers()), st.integers(min_value=1))
def test_res2tile(coords, tile_size):
    x, y = coords
    result = res2tile((x, y), tile_size)
    assert result ==  Coord(x // tile_size, y // tile_size)

if __name__ == '__main__':
    pytest.main()