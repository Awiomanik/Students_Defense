#IMPORTS
from dataclasses import dataclass
import typing, pygame, os


# CLASSES
@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __add__(self, other: typing.Union['Coord', int, float]) -> 'Coord':
        """Add another Coord instance or a numeric value to this coordinate.
            Parameters:
                other: (Union[Coord, int, float]): The other coordinate to add or a numeric value to be added to both coordinates.

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
            str: The string representation of the coordinate, formatted as '|x,y|'.
        """
        return f"x.{self.x}, y.{self.y}"

    def __iter__(self) -> typing.Generator[int, None, None]:
        """Allow the Coord to be iterated over, yielding its x and y coordinates."""
        yield self.x
        yield self.y

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

    def grid_middle_point(coords : 'Coord', tile_size : int = 120) -> 'Coord':
        """Takes grid position and return pixel position of middle point in tile."""
        return Coord(coords.x*tile_size + tile_size//2, coords.y*tile_size + tile_size//2)