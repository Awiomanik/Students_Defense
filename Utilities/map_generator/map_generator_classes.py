"""Map holding class for map-generator"""


# IMPORTS
import pygame
from dataclasses import dataclass
from random import randint, shuffle
import os
import typing


# Data type to standardize screen coordinates
#   o--------->
#   |         x
#   |
#   |
#   v y
@dataclass
class Coord:
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, Coord):
            return Coord(self.x + other.x, self.y + other.y)
        elif isinstance(other, (int, float)):  # Allows addition with a number to both x and y
            return Coord(self.x + other, self.y + other)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Coord):
            return Coord(self.x - other.x, self.y - other.y)
        elif isinstance(other, (int, float)):  # Allows subtraction with a number from both x and y
            return Coord(self.x - other, self.y - other)
        else:
            return NotImplemented

    def __repr__(self):
        return f"{self.x}, {self.y}"
    

# GENERATED MAP CLASS
class Map:
    # possible tile contents (string):
    # ' ' (empty): grass or sand, tower placement possible
    # 'x' (obsticle): tower placement not possible
    # '#' (path): tower placement not possible
    # 'S' (start): : tower placement not possible
    # 'E' (end): : tower placement not possible
    # '*' (tower): : tower placement not possible

    def __init__(self,
                 tileset_path : str,
                 screen : pygame.Surface, 
                 resolution : tuple[int, int] = (1920, 1080), 
                 tile_size : int = 60) -> None:
        
        # initialize tiles
        self.screen = screen
        self.tile_size = tile_size
        self.grid_size = Coord(resolution[0] // tile_size, resolution[1] // tile_size)
        self.tiles = [[None for _ in range(self.grid_size.x)] for _ in range(self.grid_size.y)]
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
        self.grid = [[' ' for _ in range(self.grid_size.x)] for _ in range(self.grid_size.y)] # list[list[str],.. ]
        self.start, self.end = None, None # Coord
        self.paths = [] # list[list[Coord,.. ],.. ]

    @classmethod
    def grass_map(cls,
                  tileset_path : str,
                  screen : pygame.Surface, 
                  resolution : int = (1920, 1080), 
                  tile_size : int = 60) -> typing.Self:
        
        # initialize class object
        board = cls(tileset_path, screen, resolution, tile_size)
        # populate tiles with grass and grid with empty spots
        board.tiles = [[board.tileset["grass"] for _ in range(board.grid_size.x)] for _ in range(board.grid_size.y)]
        board.grid = [[' ' for _ in range(board.grid_size.x)] for _ in range(board.grid_size.y)]
        # return class object with grass tiles
        return board

    @classmethod
    def random_map(cls,
                  tileset_path : str,
                  screen : pygame.Surface,
                  obsticle_density : int = 5, 
                  resolution : int = (1920, 1080), 
                  tile_size : int = 60) -> typing.Self:
        
        # Initialize with grass
        board = cls.grass_map(tileset_path, screen, resolution, tile_size)

        # Set initial path
        board.start = Coord(randint(5, board.grid_size.x - 5), randint(5, board.grid_size.y - 5))
        board.grid[board.start.y][board.start.x] = 'S'  # Mark the starting point
        board.tiles[board.start.y][board.start.x] = board.tileset["path hor"]
        
        board.grid[board.start.y - 1][board.start.x] = 'x'
        board.grid[board.start.y - 1][board.start.x - 1] = 'x'
        board.grid[board.start.y - 1][board.start.x + 1] = 'x'
        board.tiles[board.start.y - 1][board.start.x] = board.tileset["cave"]
        board.tiles[board.start.y - 1][board.start.x - 1] = board.tileset["slope l"]
        board.tiles[board.start.y - 1][board.start.x + 1] = board.tileset["slope r"]
        current_pos = Coord(board.start.x, board.start.y)
        temp_path = [current_pos]
        current_pos += Coord(0, 1)
        temp_path.append(current_pos)


        # Generate random path
        directions = [Coord(0, 1), Coord(1, 0), Coord(0, -1), Coord(-1, 0)]
        last_direction = Coord(0, 1)
        path_length = 200

        for _ in range(path_length):
            temp_directions = (directions + [last_direction] * 2)
            shuffle(temp_directions)
            
            for direction in temp_directions:
                next_pos = Coord(current_pos.x + direction.x, current_pos.y + direction.y)

                # if within the map
                if 0 <= next_pos.x < board.grid_size.x and 0 <= next_pos.y < board.grid_size.y:

                    ####################################################### ten warunek trzeba poprawić
                    if next_pos != current_pos - last_direction and (\
                       board.grid[next_pos.y][next_pos.x] == ' ' or \
                       board.grid[next_pos.y][next_pos.x] == '#'):
                        temp_path.append(next_pos)
                        current_pos = next_pos
                        last_direction = direction
                        break


        # Set end-point
        board.end = temp_path[-1]
        last = temp_path[-2]
        if last.x > board.end.x: 
            board.tiles[board.end.y][board.end.x] = board.tileset['chest l']
        if last.x < board.end.x: 
            board.tiles[board.end.y][board.end.x] = board.tileset['chest r']
        if last.y > board.end.y: 
            board.tiles[board.end.y][board.end.x] = board.tileset['chest t']
        if last.y < board.end.y: 
            board.tiles[board.end.y][board.end.x] = board.tileset['chest b']

        board.grid[board.end.y][board.end.x] = 'E'
        #temp_path = [(1,1), (2,1), (3,1), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), 
        #             (4,7), (4,8), (4,9), (5,9), (6,9), (7,9), (8,9), (9,9), (9,8), 
        #             (9,7), (9,6), (9,5), (8,5), (7,5), (6,5), (5,5), (4,5), (3,5), 
        #             (2,5), (1,5), (1,6), (1,7), (1,8), (2,8), (3,8), (4,8), (5,8),
        #             (6,8), (7,8), (8,8), (8,9), (8,10), (8,11), (8,12), (8,13)]
        #temp_path = [Coord(x, y) for x, y in temp_path]
        
        board.paths.append(temp_path)

        # Mark the path in the grid and update tiles with path

        for i, pos in enumerate(temp_path[1:-1], 1):
            board.grid[pos.y][pos.x] = '#'
            board.tiles[pos.y][pos.x] = board.select_tile_type(i, pos)


        for row in range(board.grid_size.x):
            for col in range(board.grid_size.y):
                if board.grid[col][row] == ' ' and randint(1, 100) < obsticle_density:
                    board.grid[col][row] = 'x'
                    board.tiles[col][row] = board.tileset[f"plant {randint(0, 17)}"]


        return board
    
        #board.tiles = [[board.tileset[randint(0, len(board.tiles[0]) - 1)][randint(0, len(board.tiles) - 1)] \
         #               for _ in range(board.rows)] \
          #                  for _ in range(board.columns)]
        #return board

    def select_tile_type(self, index : int, coords : Coord, path_number : int = 0) -> pygame.Surface:
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
            return self.tileset["path ver"]
        
        if previous.x == current.x == following.x:
            return self.tileset["path hor"]

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
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile is not None:
                    self.screen.blit(tile, (x * self.tile_size, y * self.tile_size))

    def add_tile(self, x, y):
        pass

    def __str__(self):
        # Create a bordered grid presentation
        tile_size = f"Size of a tile:   {self.tile_size}px by {self.tile_size}px"
        grid_size = f"Size of the grid: {self.grid_size.x} tiles by {self.grid_size.y} tiles"
        grid_lines = ['| ' + ' '.join(row) + ' |' for row in self.grid]
        top_border = '+' + '-' * (2 * len(self.grid[0]) + 1) + '+'
        bottom_border = top_border
        framed_grid = [top_border] + grid_lines + [bottom_border]

        # Convert the grid and path lists into strings
        grid_str = '\n'.join(framed_grid)
        paths_str = '\n'.join([f"Path {i}:\n{path}" for i, path in enumerate(self.paths) if path])
        start_str = f"Start: \t{self.start}" if self.start else "Start: \tNone"
        end_str = f"End: \t{self.end}" if self.end else "End: \tNone"

        return f"Grid:\n{grid_str}\n\n{tile_size}\n{grid_size}\n\n{start_str}\n{end_str}\n\nPaths:\n{paths_str}\n"





