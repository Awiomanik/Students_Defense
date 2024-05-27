"""Map holding class for map-generator"""


# IMPORTS
import pygame
import os
import typing
from ..Utilities import Coord


# GENERATED MAP CLASS
class Map:
    """
    A class used to represent the game map for Students Defense Game.

    This class provides functionalities to initialize different types of maps, including random generation
    of paths and obstacles. It also handles graphical rendering of the map on a given Pygame surface.

    Attributes:
        screen (pygame.Surface): The Pygame surface where the map will be drawn.
        tile_size (int): The size of each tile (both width and height).
        grid_size (Coord): The dimensions of the map grid, calculated from the resolution and tile size.
        tiles (dict[Coord : pygame.Surface]]): 2D list of Pygame surfaces representing the visual content of each tile.
        grid (dict[Coord : str]]): 2D list representing the type of each tile in the grid.
        paths (list[list[Coord]]): List of paths, where each path is a list of coordinates.
        tileset (dict[str, pygame.Surface]): Dictionary mapping tile names to their Pygame surfaces.

    Methods:
        __init__: Initializes a new Map instance.
        grass_map: Class method to create a map filled entirely with grass tiles.
        random_map: Class method to generate a map with random paths and obstacles.
        select_path_type: Determines the correct tile type based on the direction of the path segment.
        draw: Draws the map on the provided Pygame surface.
    """
    # possible tile contents (string):
    # ' ' (empty): grass or sand, tower placement possible
    # 'x' (obsticle): tower placement not possible
    # '^', 'v', '<', '>', '+' (path): tower placement not possible
    # 'S' (start): : tower placement not possible
    # 'E' (end): : tower placement not possible
    # '*' (tower): : tower placement not possible

    def __init__(self,
                 tileset_path : str,
                 screen : pygame.Surface, 
                 resolution : tuple[int, int] = (1920, 1080), 
                 tile_size : int = 120) -> None:
        
        # initialize tiles
        self.screen = screen
        self.tile_size = tile_size
        self.grid_size = Coord(resolution[0] // tile_size, resolution[1] // tile_size)
        self.tiles = {key : None for key in [Coord(x, y) for x in range(self.grid_size.x) for y in range(self.grid_size.y)]} # set[Coord : pygame.Surface]
        # temporary helping varibles
        keys = ["grass", 
                "path ver", "path hor", 
                "path l-t", "path l-b", "path r-t", "path r-b", 
                "path cros",
                "end l", "end r", "end t", "end b",
                "cave", "chest", "slope l", "slope r",
                "chest l", "chest r", "chest t", "chest b"] + \
                [f"plant {i}" for i in range(18)]
        values = ["grass.png", 
                  "path_ver.png", "path_hor.png", 
                  "path_cor_t_l.png", "path_cor_b_l.png", "path_cor_t_r.png", "path_cor_b_r.png", 
                  "path_cros.png",
                  "path_end_l.png", "path_end_r.png", "path_end_t.png", "path_end_b.png",
                  "cave.png", "chest.png", "slope_l.png", "slope_r.png",
                  "chest_l.png", "chest_r.png", "chest_t.png", "chest_b.png"] + \
                  [f"plant{i}.png" for i in range(18)]
        self.tileset = {key : pygame.image.load(os.path.join(tileset_path, value)).convert_alpha()
                        for key, value in zip(keys, values)}

        # initialize grid content
        self.grid = {key : None for key in [Coord(x, y) for x in range(self.grid_size.x) for y in range(self.grid_size.y)]} # set[Coord : str]
        self.paths = [[]] # list[list[Coord,.. ],.. ]

    @classmethod
    def grass_map(cls,
                  tileset_path : str,
                  screen : pygame.Surface, 
                  resolution : int = (1920, 1080), 
                  tile_size : int = 120) -> typing.Self:
        
        # initialize class object
        board = cls(tileset_path, screen, resolution, tile_size)
        # populate tiles with grass and grid with empty spots
        board.tiles = {Coord(x, y) : board.tileset["grass"] for x in range(board.grid_size.x) for y in range(board.grid_size.y)}
        board.grid = {Coord(x, y) : ' ' for x in range(board.grid_size.x) for y in range(board.grid_size.y)}
        # Add first and last path
        first, secound,  last = Coord(0, 4), Coord(1, 4), Coord(board.grid_size.x - 1, 4)
        board.tiles[first] = board.tileset["path hor"]
        board.tiles[secound] = board.tileset["end r"]
        board.tiles[last] = board.tileset["end l"]
        board.grid[first] = board.grid[secound] = board.grid[last] = '>'
        board.paths[0] = [first, secound, last]
        # return class object with grass tiles
        return board
    
    def select_path_type(self, index : int, coords : Coord, path_number : int = 0) -> pygame.Surface:
        # Unpack path segment
        curr_path = self.paths[path_number]
        previous = curr_path[index - 1]
        current = curr_path[index]
        following = curr_path[index + 1]

        # Determine tile already visited, simplifying the logic to check for a crossing first
        if coords in curr_path[:index]:
            return self.tileset["path cros"]  # Crossing

        # Check for horizontal and vertical paths
        if previous.y == current.y == following.y:
            return self.tileset["path hor"]
        
        if previous.x == current.x == following.x:
            return self.tileset["path ver"]

        # Determine corner types by comparing the transitions
        if previous.x != current.x and current.y != following.y:
            if previous.x < current.x:
                if current.y < following.y:
                    return self.tileset["path l-b"]  # Corner (left-bottom)
                else:
                    return self.tileset["path l-t"]  # Corner (left-top)
            else:
                if current.y < following.y:
                    return self.tileset["path r-b"]  # Corner (right-bottom)
                else:
                    return self.tileset["path r-t"]  # Corner (right-top)
                
        elif previous.y != current.y and current.x != following.x:
            # v
            # .
            if previous.y < current.y:
                # v
                # >
                if current.x < following.x:
                    return self.tileset["path r-t"]  # Corner (right-bottom)
                # v
                # <
                else:
                    return self.tileset["path l-t"]  # Corner (left-bottom)
            # .
            # ^
            else:
                # >
                # ^
                if current.x < following.x:
                    return self.tileset["path r-b"]  # Corner (right-top)
                # <
                # ^
                else:
                    return self.tileset["path l-b"]  # Corner (left-top)

        # Default case if none of the above conditions are met
        return self.tileset["grass"]  # Use grass as a fallback

    def draw(self):
        for x in range(self.grid_size.x):
            for y in range(self.grid_size.y):
                tile = self.tiles[Coord(x, y)]
                if tile is not None:
                    self.screen.blit(tile, (x * self.tile_size, y * self.tile_size))

    def tile_accessibility(self, pos : tuple[int, int], draw_rect : bool = True) -> bool:
        # Get pos in tile coordinates
        pos = Coord(pos[0] // self.tile_size, pos[1] // self.tile_size)     

        previous = self.paths[0][-2]
        previous_direction = self.paths[0][-3] - self.paths[0][-2]
        accessible = [previous + shift for x, y in [(0, 1), (1, 0), (-1, 0), (0, -1)] \
                      if (shift:=Coord(x, y)) != previous_direction]
        
        if pos in accessible:
            color = pygame.Color(0, 255, 0, 128)
            return_value = True
        else: 
            color = pygame.Color(255, 0, 0, 100)
            return_value = False
        
        if draw_rect:
            # Create a new temporary surface with per-pixel alpha
            path_cut = (self.tile_size//8)
            path_size = self.tile_size - 2 * path_cut
            temp_surface = pygame.Surface((path_size, path_size), pygame.SRCALPHA)
            temp_surface.fill((0, 0, 0, 0))  # Fill the surface with a fully transparent color

            # Draw a rounded rectangle on the temporary surface
            pygame.draw.rect(temp_surface, color, 
                            pygame.Rect(0, 0, path_size, path_size), 
                            border_radius=int(self.tile_size / 5))  # Adjust border radius here

            # Draw the temporary surface onto the main screen at the specified position
            self.screen.blit(temp_surface, (pos.x * self.tile_size + path_cut, pos.y * self.tile_size + path_cut))

        return return_value

    def add_path(self, pos : tuple[int, int]) -> None:
        # check if the end 

        # Get pos in tile coordinates
        pos = Coord(pos[0] // self.tile_size, pos[1] // self.tile_size)

        # Append new tile to path
        index = len(self.paths[0]) - 1
        self.paths[0].insert(index, pos)
        previous = self.paths[0][-3]

        direction = Coord(pos.x - previous.x, pos.y - previous.y)

        if direction == Coord(1, 0):  # Right
            tile_type = '>'
            path_end = self.tileset["end r"]
        elif direction == Coord(-1, 0):  # Left
            tile_type = '<'
            path_end = self.tileset["end l"]
        elif direction == Coord(0, 1):  # Down
            tile_type = 'v'
            path_end = self.tileset["end b"]
        elif direction == Coord(0, -1):  # Up
            tile_type = '^'
            path_end = self.tileset["end t"]

        self.tiles[self.paths[0][index - 1]] = self.select_path_type(index - 1, pos)

        self.grid[self.paths[0][index]] = tile_type
        self.tiles[self.paths[0][index]] = path_end

        
    def __str__(self):
        # Create a bordered grid presentation
        top_border = '+-' + '-' * (2 * self.grid_size.x) + '+'
        bottom_border = top_border
        rows = ['| ' + ' '.join([tile for tile in [self.grid[Coord(x, y)] for x in range(self.grid_size.x)]]) + ' |' for y in range(self.grid_size.y)]
        
        # Convert the grid and path lists into strings
        grid_str = '\n'.join([top_border] + rows + [bottom_border])
        paths_str = '\n'.join([f"Path {i}:\n{', '.join(map(str, path))}" for i, path in enumerate(self.paths) if path])
        tile_size = f"Size of a tile:   {self.tile_size}px by {self.tile_size}px"
        grid_size = f"Size of the grid: {self.grid_size.x} tiles by {self.grid_size.y} tiles"

        return f"Grid:\n{grid_str}\n\nTile Size:\n{tile_size}\nGrid Size:\n{grid_size}\n\nPaths:\n{paths_str}\n"





