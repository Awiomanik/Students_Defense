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
        keys = ["grass", "grass bottom", "grass on sand left", "grass on sand right", "grass on sand middle", 
                "path ver", "path hor", 
                "path l-t", "path l-b", "path r-t", "path r-b", 
                "path cros",
                "end l", "end r", "end t", "end b",
                "cave", "chest", "slope l", "slope r",
                "chest l", "chest r", "chest t", "chest b",
                "water wall sand left", "water wall sand right", "wall sand left", "wall sand right",
                "water sand left", "water sand bottom", "water sand right", "sand horizontal"] + \
                [f"plant {i}" for i in range(18)]
        values = ["grass.png", "grass_bot.png", "grass_bot_sand_l.png", "grass_bot_sand_r.png", "grass_bot_sand.png",
                  "path_ver.png", "path_hor.png", 
                  "path_cor_t_l.png", "path_cor_b_l.png", "path_cor_t_r.png", "path_cor_b_r.png", 
                  "path_cros.png",
                  "path_end_l.png", "path_end_r.png", "path_end_t.png", "path_end_b.png",
                  "cave.png", "chest.png", "slope_l.png", "slope_r.png",
                  "chest_l.png", "chest_r.png", "chest_t.png", "chest_b.png",
                  "water_wall_sand_l.png", "water_wall_sand_r.png", "wall_sand_l.png", "wall_sand_r.png", 
                  "water_sand_l.png", "water_sand_bot.png", "water_sand_r.png", "sand_hor.png"] + \
                  [f"plant{i}.png" for i in range(18)]
        self.tileset = {key : pygame.image.load(os.path.join(tileset_path, value)).convert_alpha()
                        for key, value in zip(keys, values)}

        # initialize grid content
        self.grid = {key : None for key in [Coord(x, y) for x in range(self.grid_size.x) for y in range(self.grid_size.y)]} # set[Coord : str]
        self.paths = [[]] # list[list[Coord,.. ],.. ]
        self.obsticles = {}

        # initialize variable for storing information if the path is finnished
        self.valid = False

    @classmethod
    def grass_map(cls,
                  tileset_path : str,
                  screen : pygame.Surface, 
                  resolution : int = (1920, 1080), 
                  tile_size : int = 120) -> typing.Self:
        
        # initialize class object
        board = cls(tileset_path, screen, resolution, tile_size)

        # populate tiles with grass and beach and grid with empty spots and obsticles
        board.tiles = {Coord(x, y) : board.tileset["grass"] \
                        for x in range(board.grid_size.x) \
                        for y in range(board.grid_size.y - 2)}
        
        board.tiles |= {Coord(x, board.grid_size.y - 3) : board.tileset["grass bottom"] \
                        for x in [0, 1, board.grid_size.x - 2, board.grid_size.x - 1]}
        
        board.tiles |= {Coord(x, board.grid_size.y - 2) : board.tileset["grass on sand middle"] \
                        for x in range(3, board.grid_size.x - 3)}
        
        board.tiles[Coord(2, board.grid_size.y - 2)] = board.tileset["grass on sand left"]
        board.tiles[Coord(board.grid_size.x - 3, board.grid_size.y - 2)] = board.tileset["grass on sand right"]
        
        board.tiles |= {Coord(x, board.grid_size.y - 1) : board.tileset["water sand bottom"] \
                        for x in range(1, board.grid_size.x - 1)}
        
        board.tiles[Coord(0, board.grid_size.y - 2)] = board.tileset["water wall sand left"]
        board.tiles[Coord(board.grid_size.x - 1, board.grid_size.y - 2)] = board.tileset["water wall sand right"]
        
        board.tiles[Coord(1, board.grid_size.y - 2)] = board.tileset["wall sand left"]
        board.tiles[Coord(board.grid_size.x - 2, board.grid_size.y - 2)] = board.tileset["wall sand right"]

        board.tiles[Coord(0, board.grid_size.y - 1)] = board.tileset["water sand left"]
        board.tiles[Coord(board.grid_size.x - 1, board.grid_size.y - 1)] = board.tileset["water sand right"]

        board.grid = {Coord(x, y) : ' ' \
                        for x in range(board.grid_size.x) \
                        for y in range(board.grid_size.y - 2)}
        
        board.grid |= {Coord(x, y) : 'x' \
                        for x in range(board.grid_size.x) \
                        for y in [board.grid_size.y - 2, board.grid_size.y - 1]}

        # Add first, secound and last path
        first, secound,  last = Coord(0, 4), Coord(1, 4), Coord(board.grid_size.x - 1, 4)
        board.tiles[first] = board.tileset["path hor"]
        board.tiles[secound] = board.tileset["end r"]
        board.tiles[last] = board.tileset["end l"]
        board.grid[first] = board.grid[secound] = board.grid[last] = '>'
        board.paths[0] = [first, secound, last]

        # Add 2 obsticles around the start
        top, bot = Coord(0, 3), Coord(0, 5)
        board.tiles[top] = board.tileset["plant 0"]
        board.tiles[bot] = board.tileset["plant 1"]
        board.grid[top] = 'x'
        board.grid[bot] = 'x'
        board.obsticles[top] = 0
        board.obsticles[bot] = 1
        
        # return class object with grass tiles
        return board
    
    def res2tile(self, coords : tuple[int, int]) -> Coord:
        return Coord(coords[0] // self.tile_size, coords[1] // self.tile_size)
    
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
        pos = self.res2tile(pos)   
        
        # Check for end tile
        end_tile = pos == self.paths[0][-1]

        previous = self.paths[0][-2]
        direction = pos - previous
        previous_direction = self.paths[0][-3] - self.paths[0][-2]
        accessible = [previous + shift for x, y in [(0, 1), (1, 0), (-1, 0), (0, -1)] \
                      if (shift:=Coord(x, y)) != previous_direction]
        
        # Check if (tile empty or part of the path) and
        # (it is the end-tile or (pos is not a reverse and 
        # (is not already taken or (is taken but the next one is empty (croosing)))))
        if (self.grid[pos] == ' ' or pos in self.paths[0]) and \
           (end_tile or (pos in accessible and \
           (pos not in self.paths[0] or (pos in self.paths[0] and pos + direction not in self.paths[0])))):
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

    def add_path(self, pos : tuple[int, int]) -> bool:
        # Get pos in tile coordinates
        curr_pos = self.res2tile(pos)

        # Check if reached end tile
        end = curr_pos == self.paths[0][-1]
        
        # Check for crossing
        crossing = curr_pos in self.paths[0]

        # Append new tile to path
        index = len(self.paths[0]) - 1
        self.paths[0].insert(index, curr_pos)
        previous = self.paths[0][-3]
        direction = curr_pos - previous

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
        
        # Path finnished
        if end:
            self.paths[0].pop()
            self.paths[0].append(Coord(16, 4))
            print(self.paths[0])
            self.tiles[self.paths[0][index - 1]] = self.select_path_type(index - 1, curr_pos - direction)

            self.tiles[self.paths[0][index]] = self.select_path_type(index, curr_pos)
            self.paths[0].pop()        
            
            self.valid = True
            return self.valid

        # Append crossing
        if crossing:
            self.paths[0].insert(index + 1, curr_pos + direction)

            self.tiles[self.paths[0][index - 1]] = self.select_path_type(index - 1, curr_pos - direction)

            self.grid[self.paths[0][index]] = '+'
            self.tiles[self.paths[0][index]] = self.tileset["path cros"]
 
            self.grid[self.paths[0][index + 1]] = tile_type
            self.tiles[self.paths[0][index + 1]] = path_end  
        # No crossing  
        else:
            self.tiles[self.paths[0][index - 1]] = self.select_path_type(index - 1, curr_pos - direction)

            self.grid[self.paths[0][index]] = tile_type
            self.tiles[self.paths[0][index]] = path_end

        return False

    def remove_path(self) -> None:
        if len(self.paths[0]) > 3:
            # Get last 3 tiles
            curr_tile = self.paths[0][-2]
            previous_tile = self.paths[0][-3]
            preprevious_tile = self.paths[0][-4]

            # Check for crossing
            crossing = self.grid[previous_tile] == '+'

            # remove last path from map
            self.grid[curr_tile] = ' '
            self.tiles[curr_tile] = self.tileset['grass']
            self.paths[0].pop(-2)          

            # Crossing -> remove another element
            if crossing:
                direction = preprevious_tile - self.paths[0][-4]
            else:
                direction = previous_tile - preprevious_tile

            if direction == Coord(1, 0):  # Right
                path_end = self.tileset["end r"]
            elif direction == Coord(-1, 0):  # Left
                path_end = self.tileset["end l"]
            elif direction == Coord(0, 1):  # Down
                path_end = self.tileset["end b"]
            elif direction == Coord(0, -1):  # Up
                path_end = self.tileset["end t"]

            # Crossing
            if crossing: 
                self.tiles[previous_tile] = self.tileset["path hor"] \
                                            if preprevious_tile - previous_tile in (Coord(0, 1), Coord(0, -1)) \
                                            else self.tileset["path ver"]
               
                self.paths[0].pop(-2)
                grid_direction = {Coord(1, 0) : '<',
                                  Coord(-1, 0) : '>',
                                  Coord(0, -1) : 'v',
                                  Coord(0, 1) : '^'}
                index_in_path = self.paths[0].index(preprevious_tile)
                self.grid[previous_tile] = grid_direction[self.paths[0][index_in_path] - self.paths[0][index_in_path - 1]]
                
                self.tiles[preprevious_tile] = path_end

            # No crossing
            else:
                self.tiles[previous_tile] = path_end
 
    def clear_paths(self) -> None:
        for path in self.paths:
            for segment in path:
                self.grid[segment] = ' '
                self.tiles[segment] = self.tileset["grass"]
        
        # Add first, secound and last path
        first, secound,  last = Coord(0, 4), Coord(1, 4), Coord(self.grid_size.x - 1, 4)
        self.tiles[first] = self.tileset["path hor"]
        self.tiles[secound] = self.tileset["end r"]
        self.tiles[last] = self.tileset["end l"]
        self.grid[first] = self.grid[secound] = self.grid[last] = '>'
        self.paths = [[first, secound, last]]
        
        self.valid = False

    def add_obsticle(self, pos : tuple[int, int]) -> None:
        if pos[1] < 840:
            pos = self.res2tile(pos)

            if self.grid[pos] == ' ':
                self.grid[pos] = 'x'
                self.tiles[pos] = self.tileset["plant 0"]
                self.obsticles[pos] = 0

            elif self.grid[pos] == 'x':
                new = (self.obsticles[pos] + 1) % 18
                self.tiles[pos] = self.tileset[f"plant {new}"]
                self.obsticles[pos] = new

    def remove_obsticle(self, pos : tuple[int, int]) -> None:
        pos = self.res2tile(pos)

        if self.grid[pos] == 'x':
            self.grid[pos] = ' '
            self.tiles[pos] = self.tileset["grass"]
            self.obsticles.pop(pos)

    def save(self) -> bool:
        if self.valid:
            clock = pygame.time.Clock()

            input_box1 = InputBox(50, 100, 140, 32)
            input_box2 = InputBox(50, 150, 140, 32)
            input_boxes = [input_box1, input_box2]

            done = False
            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    for box in input_boxes:
                        box.handle_event(event)

                for box in input_boxes:
                    box.update()

                self.screen.fill((0, 0, 0))
                for box in input_boxes:
                    box.draw(self.screen)

                pygame.display.flip()
                clock.tick(30)
                
            return True
        
        else:
            return False

    def __str__(self):
        # Create a bordered grid presentation
        top_border = '+-' + '-' * (2 * self.grid_size.x) + '+'
        bottom_border = top_border
        rows = ['| ' + ' '.join([tile for tile in [self.grid[Coord(x, y)] for x in range(self.grid_size.x)]]) + ' |' for y in range(self.grid_size.y)]
        
        # Convert the grid and path lists into strings
        grid_str = '\n'.join([top_border] + rows + [bottom_border])
        paths_str = '\n'.join([f"Path {i}:\n{' > '.join(map(str, path))}" for i, path in enumerate(self.paths) if path])
        tile_size = f"Size of a tile:   {self.tile_size}px by {self.tile_size}px"
        grid_size = f"Size of the grid: {self.grid_size.x} tiles by {self.grid_size.y} tiles"

        return f"Grid:\n{grid_str}\n\nTile Size:\n{tile_size}\nGrid Size:\n{grid_size}\n\nPaths:\n{paths_str}\n"


# INUT BOX FOR SAVE WINDOW WITHIN WINDOW
class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.font = pygame.font.Font(None, 32)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = ()
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = (255, 255, 255) if self.active else (200, 200, 200)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''  # Reset text after submission
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, (0, 0, 0))

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)




