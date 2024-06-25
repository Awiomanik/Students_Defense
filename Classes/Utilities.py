"""
This module contains utility classes and functions that are widely used across the 
Students Defense Game project. It includes data structures, commonly used constants, 
and helper functions to ensure consistency and reusability of code.

Classes:
    Coord - Represents a point in 2D coordinate space with operations for basic arithmetic. Designed to standardize tile coordinates and screen coordinates
    InputBox - Represents an input box in the game, provides functionality for creating an input box that can handle user input.

Functions:
    xor(text : str, key : str, decrypt : bool = False) -> str: Encrypts or decrypts a given text using XOR cipher with a provided key.
    load_high_scores(root_directory : str) -> tuple[tuple[str, int]]: Loads High Score records from a designated file.
    save_high_score(root_directory : str, name : str, score : int) -> None: Saves a new high score record to the high score file.
    """


#IMPORTS
from dataclasses import dataclass
import typing, pygame, os
from math import ceil


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
        __add__(self, other : typing.Union['Coord', int, float]) -> 'Coord': Supports adding another Coord instance or a numeric value to this coordinate.
        __sub__(self, other : typing.Union['Coord', int, float]) -> 'Coord': Supports subtracting another Coord instance or a numeric value from this coordinate.
        __repr__(self) -> str: Returns a string representation of the coordinate.
        __iter__(self) -> typing.Generator[int, None, None]: Creates iterator object yielding Coord coordinates (x, then y).
        res2tile(coords : tuple[int, int], tile_size : int = 120) -> 'Coord': Returns coords converted from screen coordinates (pixels) to grid coordinates.
        grid_middle_point(self : 'Coord', tile_size : int = 120) -> 'Coord': Takes grid position and return pixel position of middle point in tile.
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
    def __eq__(self, other: 'Coord') -> bool:
        """Defines equality as having same .x and .y"""
        if isinstance(other, Coord):
            if self.x == other.x and self.y == other.y:
                return True
            else:
                return False
        else:
            return False

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
        """ Takes grid position and return pixel position of middle point in tile """
        return Coord(coords.x*tile_size + tile_size//2, coords.y*tile_size + tile_size//2)
    
    def ceiling(self) -> 'Coord':
        return Coord(ceil(self.x),ceil(self.y))

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


# FUNCTIONS
def xor(text : str, key : str, decrypt : bool = False) -> str:
    """
    Encrypts or decrypts a given text using XOR cipher with a provided key.

    The XOR cipher is a symmetric encryption algorithm that operates by taking 
    the exclusive OR of each character in the input text with a character 
    from the key.

    The function operates as follows:
    1. For each character in the input text, it computes the XOR of the ASCII 
       value of the character with the ASCII value of the corresponding character 
       in the key. 
    2. The key is repeated cyclically to match the length of the text.
    3. The resulting ASCII values are converted to hexadecimal to ensure 
       all characters are printable.

    Parameters:

        text (str): The input text to be encrypted or decrypted. This can be any string of characters.

        key (str):  The key used for the XOR operation. The key can be of any length; if the 
                    key is shorter than the text, it will be repeated cyclically to match 
                    the length of the text.
        
        decrypt (bool): Wheter to perform decryption process (True) or encryption (False).
                        It's important for hexadecimal convertion. (defaults to False)

    Returns:

    str:    The resulting text after applying the XOR operation and encoding/decoding 
            in hexadecimal. If the input was plaintext, the output will be ciphertext, 
            and vice versa.


    Notes:
    - The XOR cipher is not secure for most practical applications, especially if 
      the key is shorter than the text or if the same key is reused. It is generally 
      used for simple obfuscation rather than secure encryption.
    - The XOR operation can result in non-printable characters, which are handled 
      by converting the result to hexadecimal format.
    """
    # Encode to hexadecimal
    if decrypt:
        text = bytes.fromhex(text).decode('utf-8')

    # XOR the text
    xor_result = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))

    # Decode from hexadecimal format
    if not decrypt:
        xor_result = xor_result.encode('utf-8').hex()

    return xor_result

def load_high_scores(root_directory : str) -> tuple[tuple[str, int]]:
    """
    Loads High Score records from a designated file.

    Parameters:
        root_directory (str): Root directory of the repository for easy relative path meneging.

    Returns:
        tuple[tuple[str, int]]: A list of tuples containing names and corresponding scores.

    Raises:
        FileNotFoundError: If the high scores file is not found.
        HighScoreFileFormatError: If the file content is not in the expected format.
    """

    path = os.path.join(root_directory, "Assets", "menu_data", "hs.dat")
    ENCRYPTION_KEY = "e^(i*pi) = -1" # Should not be changed to decrypt the encrypted data

    # Check if the file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"High Score file not found: {path}")
    
    # Open and read the file
    with open(path, 'r') as file:
        records = file.readlines()

        try:
            # Decrypt the data discarding comments in the file
            records = [xor(line, ENCRYPTION_KEY, True) for line in records if not line.startswith('#')]
            # Split the records to names and corresponding scores
            records = [line.strip().split(',') for line in records]
            # Format the file content to a list of tuples
            records = [(record[0].strip(), int(record[1].strip())) for record in records]
        
        except ValueError as ve:
            # Create custom Error class
            class HighScoreFileFormatError(Exception):
                def __init__(self, issue: str, file_path: str) -> None:
                    self.issue = issue
                    self.file_path = file_path
                    self.message = (f"File at {self.file_path} includes formatting error: {self.issue}. "
                                    "High Score records should be divided by a new line symbol "
                                    "and be formatted as 'Name, Score'. "
                                    "All other white characters at the beginning and end of records "
                                    "will be stripped and do not affect them. "
                                    "All lines starting with a hash symbol ('#') "
                                    "will be omitted by the file reading function.")
                    super().__init__(self.message)
            
            # Raise custom error
            raise HighScoreFileFormatError(f"Invalid score format: {ve}", path)
    
    # Sort records in descending order
    records.sort(key=(lambda x: int(x[1])), reverse=True)

    return tuple(records)

def save_high_score(root_directory : str, name : str, score : int) -> None:
    """
    Saves a new high score record to the high score file.

    This function encrypts the high score data before writing it to the file to ensure that it
    cannot be easily modified by a user.

    Parameters:
        root_directory (str): The root directory of the repository for easy relative path management.
        name (str): The name of the player.
        score (int): The score achieved by the player.

    Raises:
        FileNotFoundError: If the high score file is not found.
        PermissionError: If there are insufficient permissions to write to the file.
        IOError: If there is an input/output error during the file operation.
        Exception: For any other unexpected exceptions.
    """
    # Get path to high scores data
    path = os.path.join(root_directory, "Assets", "menu_data", "hs.dat")

    # Set decryption key as the same value as when encrypting
    DECRYPTION_KEY = "e^(i*pi) = -1"  # Should not be changed to decrypt the encrypted data

    # Open the file and write new score
    try:
        with open(path, 'a') as file:
            encrypted_data = xor(f"\n{name}, {score}", DECRYPTION_KEY)
            file.write(encrypted_data)

    except FileNotFoundError:
        raise FileNotFoundError(f"High Score file not found: {path}")
    
    except PermissionError:
        raise PermissionError(f"Insufficient permissions to write to the file: {path}")
    
    except IOError as e:
        raise IOError(f"An I/O error occurred: {e}")
    
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")




















