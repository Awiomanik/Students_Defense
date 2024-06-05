"""
This module contains utility classes and functions that are widely used across the 
Students Defense Game project. It includes data structures, commonly used constants, 
and helper functions to ensure consistency and reusability of code.

Classes:
    Coord - Represents a point in 2D coordinate space with operations for basic arithmetic. Designed to standardize tile coordinates and screen coordinates

Functions:
    (If you have any specific functions, list them here with a brief description.)
"""


#IMPORTS
from dataclasses import dataclass
import typing


# CLASSES
@dataclass(frozen=True)
class Coord:
    """
    A class to represent a point in 2D coordinate space.
    
    This class provides functionality for basic arithmetic operations allowing
    addition and subtraction of coordinates, as well as scalar addition and subtraction.
    Designed to stnadardize tile coordinates and screen coordinates.
    All coordinate in the project should be represented as x (left to right), y (top to bottom):
    o--------->
    |         x
    |
    |
    v y

    Attributes:
        x (int): The x-coordinate of a point in 2D space.
        y (int): The y-coordinate of a point in 2D space.

    Methods:
        __add__: Supports adding another Coord instance or a numeric value to this coordinate.
        __sub__: Supports subtracting another Coord instance or a numeric value from this coordinate.
        __repr__: Returns a string representation of the coordinate.
    """

    x: int
    y: int

    def __add__(self, other : typing.Union['Coord', int, float]) -> 'Coord':
        """Add another Coord instance or a numeric value to this coordinate.
        
        Parameters:
            other (Union[Coord, int, float]): The other coordinate to add or a numeric value to be added to both coordinates.

        Returns:
            Coord: A new Coord instance representing the sum of the coordinates.

        Raises:
            NotImplementedError: If other is not a Coord, int, or float.
        """
        if isinstance(other, Coord):
            return Coord(self.x + other.x, self.y + other.y)
        elif isinstance(other, (int, float)):  
            return Coord(self.x + other, self.y + other)
        else:
            raise NotImplementedError()

    def __sub__(self, other : typing.Union['Coord', int, float]) -> 'Coord':
        """Subtract another Coord instance or a numeric value from this coordinate.
        
        Parameters:
            other (Union[Coord, int, float]): The other coordinate to subtract or a numeric value to be subtracted to both coordinates.

        Returns:
            Coord: A new Coord instance representing the difference of the coordinates.

        Raises:
            NotImplementedError: If other is not a Coord, int, or float.
        """
        if isinstance(other, Coord):
            return Coord(self.x - other.x, self.y - other.y)
        
        elif isinstance(other, (int, float)):
            return Coord(self.x - other, self.y - other)
        
        else:
            raise NotImplementedError()

    def __repr__(self) -> str:
        """Return a string representation of the coordinate.

        Returns:
            str: The string representation of the coordinate, formatted as 'x, y'.
        """
        return f"{self.x}, {self.y}"
    
    def res2tile(coords : tuple[int, int], tile_size : int = 120) -> 'Coord':
        """
        Scales coord from screen coordinates to grid coordinates using number of pixels tile_size.
        
        Parameters:
            coord : Coord - Screen coordinates in pixels
            tile_size : int - Size of a single tile in a grid in pixels (default 120)

        Returns: 
            Coord - Grid coordinates
        """
        return Coord(coords[0] // tile_size, coords[1] // tile_size)
