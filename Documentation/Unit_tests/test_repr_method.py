import hypothesis.strategies as st
from hypothesis import given
import pytest
from functions_from_utilities import Coord


@given(st.integers(), st.integers())
def test_repr_of_coord(x, y):
    coord = Coord(x, y)
    result = repr(coord)
    assert result == f"x.{x}, y.{y}"
