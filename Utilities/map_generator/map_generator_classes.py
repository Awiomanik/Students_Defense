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
@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, Coord):
            return Coord(self.x + other.x, self.y + other.y)
        
        elif isinstance(other, (int, float)):  
            return Coord(self.x + other, self.y + other)
        else:

            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Coord):
            return Coord(self.x - other.x, self.y - other.y)
        
        elif isinstance(other, (int, float)):
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
    # '^', 'v', '<', '>', '+' (path): tower placement not possible
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
                  path_length : int = 500,
                  resolution : int = (1920, 1080), 
                  tile_size : int = 60) -> typing.Self:
        
        # Initialize with grass
        board = cls.grass_map(tileset_path, screen, resolution, tile_size)

        # Set path
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
        path = [current_pos]
        # Set first path to go straight out of cave
        current_pos += Coord(0, 1)
        board.grid[current_pos.y][current_pos.x] = 'v'
        path.append(current_pos)

        # Generate random path
        # Initialize usefull varibles
        directions = [Coord(0, 1), Coord(1, 0), Coord(0, -1), Coord(-1, 0)]  # Down, Right, Up, Left
        direction_symbols = {Coord(0, 1): 'v', Coord(1, 0): '>', Coord(0, -1): '^', Coord(-1, 0): '<'}
        perpendicular = {'^': ('<', '>'), 'v': ('<', '>'), '<': ('^', 'v'), '>': ('^', 'v'), }
        last_direction = Coord(0, 1)

        # loop through path tiles and choose the path
        for _ in range(path_length):
            # Enhance the probability of continuing in the same direction
            temp_directions = [last_direction] * 5 + directions  # Weight the current direction more
            shuffle(temp_directions)

            for direction in temp_directions:
                if direction.x != -last_direction.x or direction.y != -last_direction.y:
                    next_pos = current_pos + direction

                    # Check if within the map boundaries
                    if 0 <= next_pos.x < board.grid_size.x and 0 <= next_pos.y < board.grid_size.y:
                        current_symbol = direction_symbols[direction]
                        next_symbol = board.grid[next_pos.y][next_pos.x]

                        # Check if tile is emptty
                        if next_symbol == ' ':
                            print(current_pos, next_pos)

                            board.grid[next_pos.y][next_pos.x] = current_symbol
                            path.append(next_pos)
                            current_pos = next_pos
                            last_direction = direction
                            break

                        # Check if path is perpendicular to the met path and if the next tile is empty
                        subsequent_pos = next_pos + direction
                        if 0 <= subsequent_pos.x < board.grid_size.x and 0 <= subsequent_pos.y < board.grid_size.y and \
                        board.grid[subsequent_pos.y][subsequent_pos.x] == ' ' and \
                        next_symbol in perpendicular[current_symbol]:
                            print(current_pos, next_pos, subsequent_pos)
                            
                            board.grid[next_pos.y][next_pos.x] = '+'
                            board.grid[subsequent_pos.y][subsequent_pos.x] = next_symbol
                            path.append(next_pos)
                            path.append(subsequent_pos)
                            current_pos = subsequent_pos
                            last_direction = direction
                            break
            
            # If no possible move, break
            else: 
                break

        # Set end-point
        board.end = path[-1]
        last = path[-2]
        if last.x > board.end.x: 
            board.tiles[board.end.y][board.end.x] = board.tileset['chest l']
        if last.x < board.end.x: 
            board.tiles[board.end.y][board.end.x] = board.tileset['chest r']
        if last.y > board.end.y: 
            board.tiles[board.end.y][board.end.x] = board.tileset['chest t']
        if last.y < board.end.y: 
            board.tiles[board.end.y][board.end.x] = board.tileset['chest b']

        board.grid[board.end.y][board.end.x] = 'E'
        
        board.paths.append(path)

        # Update tiles with path
        for i, pos in enumerate(path[1:-1], 1):
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





