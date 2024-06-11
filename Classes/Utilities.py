"""
This module contains utility classes and functions that are widely used across the 
Students Defense Game project. It includes data structures, commonly used constants, 
and helper functions to ensure consistency and reusability of code.

Classes:
    Coord - Represents a point in 2D coordinate space with operations for basic arithmetic. Designed to standardize tile coordinates and screen coordinates
    InputBox - Represents an input box in the game, provides functionality for creating an input box that can handle user input.

Functions:
    (If you have any specific functions, list them here with a brief description.)
"""


#IMPORTS
from dataclasses import dataclass
import typing, pygame


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
            str: The string representation of the coordinate, formatted as '|x,y|'.
        """
        return f"x.{self.x}, y.{self.y}"
    
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

    def grid_middle_point(self : 'Coord', tile_size : int = 120) -> 'Coord':
        """
        Takes grid position and return pixel position of middle point in tile
        """
        return Coord(self.x*tile_size + tile_size/2, self.y*tile_size + tile_size/2)

class InputBox:
    """
    A class to represent an input box in the game.

    This class provides functionality for creating an input box that can handle user input,
    update its display, and draw itself on the screen.

    Attributes:
        font (pygame.font.Font): The font used to render the text.
        rect (pygame.Rect): The rectangle representing the input box's position and size.
        color (tuple): The color of the input box.
        text (str): The text currently entered in the input box.
        txt_surface (pygame.Surface): The surface representing the rendered text.
        active (bool): A flag indicating whether the input box is active.
        color_active (tuple[int, int, int]): RGB value of the color of the box and text when active.
        color_inactive (tuple[int, int, int]): RGB value of the color of the box and text when inactive.
        current_color (tuple[int, int, int]): RGB value of the current color of the box and text.
        display_box (bool): If box should be displayed or just the text within.

    Methods:
        handle_event(event): Handles input events, such as mouse clicks and key presses.
        draw(screen): Draws the input box and its text on the screen.
    """
    def __init__(self, x : int, y : int, w : int, h : int, 
                 text : str = '', 
                 color_active : tuple[int, int, int] = (100, 50, 0),
                 color_inactive : tuple[int, int, int] = (0, 0, 0),
                 display_box : bool = False,
                 font : pygame.font = None,
                 activate = False) -> None:
        """
        Initialize an InputBox instance.

        Parameters:
            x (int): The x-coordinate of the top-left corner of the input box.
            y (int): The y-coordinate of the top-left corner of the input box.
            w (int): The width of the input box.
            h (int): The height of the input box.
            text (str): The initial text to display in the input box (default is an empty string).
            color_active (tuple[int, int, int]): RGB value of the color of the box and text when active (default is (100, 50, 0)).
            color_inactive (tuple[int, int, int]): RGB value of the color of the box and text when inactive (default is (0, 0, 0)).
            display_box (bool): Wheter box should be displayed or just the text within (default is False).
            font (pygame.font): The font used to render the text (default is pygame.font.Font(None, 32)).
            activate (bool): Wheter the input box should be active when initialized (default is False).
        """
        if font is None:
            self.font = pygame.font.Font(None, 32)
        else: 
            self.font = font
        self.rect = pygame.Rect(x, y, w, h)
        self.color_active = color_active
        self.color_inactive = color_inactive
        self.text = text
        self.active = activate
        self.current_color = color_active if self.active else color_inactive
        self.txt_surface = self.font.render(text, True, self.current_color)
        self.display_box = display_box

    def handle_event(self, event : pygame.event) -> None:
        """
        Handle input events for the input box.

        This method handles mouse click events to activate or deactivate the input box,
        and key press events to update the text in the input box.

        Parameters:
            event (pygame.event.EventType): The event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
        
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.active: 
                        self.active = False

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    self.text += event.unicode

                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.current_color)
                # Check if name not too long
                if self.txt_surface.get_width() + 10 > self.rect.width:
                    self.text = self.text[:-1]
                    self.txt_surface = self.font.render(self.text, True, self.current_color)
        
        # Change the current color of the input box.
        self.current_color = self.color_active if self.active else self.color_inactive

    def draw(self, screen : pygame.Surface) -> None:
        """
        Draw the input box on the screen.

        This method draws the input box's text and rectangle on the provided screen surface.

        Parameters:
            screen (pygame.Surface): The surface on which to draw the input box.
        """
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        if self.display_box: 
            pygame.draw.rect(screen, self.current_color, self.rect, 2)
























