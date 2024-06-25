from hypothesis import given
import hypothesis.strategies as st 
from functions_from_utilities import Coord

@given(st.integers(), st.integers())
def test_iter(x, y):
        coord = Coord(x,y)
        iter_values = list(coord)
        assert iter_values == [x, y]