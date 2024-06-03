## Connstants:
- 60 fps
- resolution: 1920, 1080
- full-screen
- grd: 16 x 9 ( 120px x 120px per tile ) (do not hard code it, we might want to change it later)
- elements are hooked to tiles (except enemies)
- bottom two rows are for HUD
- Start is on the left of the screen at x=-1, y=4 (enemies are sapwning out of the map range) (end is on the right at x=16, y=4)
- coordinates used in every class (except enemies) are: x (from left to right 0-15), y (from top to bottom 0-8). Possibpe expantion later.

## Prototype:
 - 1 map
 - 3 waves
 - 1 type of tower
 - 1 type of enemy
 - 1 tower upgreade
 - enemies follow straight parallel paths within the cellular path. They need to have position atribute in resolution coordinates, not only tile coordinates (still following the rule: from left to right, from top to bottom)


## Classes:

### Map:
A class to manage and interact with map data. This class allows for 
the loading, parsing, and representation of map data which includes grid-based accessibility of tiles, 
paths for entities within the game and map name.

Attributes:
    name (str): The name of the map.
    paths (tuple): Immutable tuple of tuples, where each inner tuple represents a path
                    as a sequence of Coord instances indicating the path through the tile grid.
    grid (list): A list of lists where each sublist represents a row in the grid.
                    Each element in the sublist is a boolean indicating the tile's accessibility.

Methods:
    __init__(self, name: str = "TEST_1", map_data_directory: str = None):
        Initializes a Map instance with a specified name and data directory. Loads the map data from the
        corresponding file within the provided or default directory.

    load_map_data(self, path: str):
        Loads and parses map data from a specified file path. This method updates the map's attributes
        based on the contents of the file including the name, grid configuration, and paths.

### Game:
This class will menage the whole game instance.

Atributes:
    ui (UI) : Instance of user interface class to menage drawing graphics (and possibly sounds)

Methods:
    __init__ :
        Does everything (for now)

### UI:
Drawing class.

Atributes:
    FPS (int) : number of frames per secound
    RESOLUTION (tuple[int, int]) : resolution of the screen
    screen (pygmae.Surface) : Screen surface
    clock (pygame.time.Clock) : Clock for menging frame-rate
    mouse_click (bool) : boolian for storing information about if mouse was clicked
    pos (tuple[int, int]) : mouse position in px coordinates 
    gfx_path (str) : path to graphic assets
    ..._gfx (pygame.Image) : graphics used in given level

Methods:
    intro:
        displays intro
    main_menu:
        displays main menu
    load_lvl:
        loads level
    update:
        updates the screen within level
