"""Prototipical map class"""

# IMPORTS
import pygame
import os


# MAP CLASS
class Map():
    """
    A class that manages the graphical representation of the game map and the paths for enemy movements.

    This class loads a background image for the map and also processes paths from a data file which enemies will follow.
    The paths include coordinates and path widths, providing a structured path system for enemy movements.

    Attributes:
    
    image (pygame.Surface): The graphical representation of the game map, loaded from the specified path and scaled to the given resolution.
    
    enemies_path (list[tuple[int, int]]): A list of tuples representing the path coordinates in pixels. Each tuple is a coordinate point on the map that defines the path enemies will follow.
    
    enemies_path_widths (list[int]): A list of integers representing the widths of the path at each segment. This width may dictate the movement constraints for enemies on the path.


    Methods:

    load_enemies_paths(path: str) -> tuple[list[tuple[int, int]], list[int]]:
        Loads enemy paths from a .dat file, extracting path coordinates and widths. This method reads from a file and parses its contents into usable path data.
        
    draw(screen: pygame.Surface) -> None:
        Draws the map image onto the provided pygame screen.
    """

    def __init__(self,
                 graphic_path : str,
                 towers_path : str,
                 resolution : tuple[int, int],
                 ) -> None:
        """
        Initializes the Map object with a background image scaled to the given resolution and loads paths for enemy movements.

        Parameters:
        graphic_path (str): Path to the graphic file of the map. This image is scaled to match the game screen resolution.
        resolution (tuple[int, int]): The resolution to which the map image will be scaled. This typically matches the game window size.
        """
        # Load image and scale it to screen size
        self.image = pygame.transform.scale(pygame.image.load(graphic_path), resolution)  

        # Load towers
        self.load_towers(towers_path)

        # Load enemies paths
        self.load_enemies_paths(graphic_path.rsplit('.', 1)[0] + '.dat')

    def load_enemies_paths(self, path : str) -> None:
        """
        Loads the enemy paths from a .dat file, returning tuples of path coordinates and path widths.

        The .dat file is expected to have path data starting from the third line, with each line containing coordinates and a path width separated by commas.

        Parameters:
        path (str): The file path to the .dat file containing the enemy path data.
        """
        # Open the file containing the paths and read all lines into path_raw
        with open(path) as file:
            path_raw = file.readlines()

        # Process each line starting from the third line
        # Strip leading/trailing whitespace and split each line on ', ' to separate the path data
        path_raw = [line.strip().split(', ') for line in path_raw[2:]]  

        # Extract the coordinates for the enemies' path from the processed data
        self.enemies_path = [(int(line[0]), int(line[1])) for line in path_raw]

        # Extract the path widths from the processed data, excluding the last data point (they are empty, there is no segment)
        self.enemies_path_widths = [int(line[2]) for line in path_raw[:-1]]
    
    ###############################################
    def load_towers(self, path : str) -> None:
        # List all files in the given directory
        files = os.listdir(path)
        
        # Filter out PNG and TXT files
        png_files = [file for file in files if file.endswith('.png')]
        txt_files = [file for file in files if file.endswith('.txt')]
        
        # Check if the number of png files matches the number of txt files
        if len(png_files) != len(txt_files):
            print("The number of PNG and TXT files does not match.")
            return [], []

        # Load contents of each file type into lists
        graphics = []
        for png_file in png_files:
            graphics.append(pygame.transform.scale(pygame.image.load(os.path.join(path, png_file)), (150, 225)))

        descriptions = []
        for txt_file in txt_files:
            with open(os.path.join(path, txt_file), 'r') as file:
                descriptions.append(file.readline().split(': ')[1])  # Read the entire contents of the file

        self.towers = list(zip(graphics, descriptions))

    def draw(self, screen : pygame.Surface) -> None:
        """
        Draws the map image onto the specified screen.

        Parameters:
            screen (pygame.Surface): The pygame screen where the map will be drawn.
        """
        screen.blit(self.image, (0, 0))