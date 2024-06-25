from ..Utilities import Coord
import os

class Map():
    """
    Manages and interacts with map data (loading, parsing, and representing map data).

    Attributes:
        name (str): The name of the map.
        paths (tuple): Immutable tuple of tuples, where each inner tuple represents a path
                       as a sequence of Coord instances indicating the path through the tile grid.
        grid (list): A list of lists where each sublist represents a row in the grid.
                     Each element in the sublist is a boolean indicating the tile's accessibility.
                     True-accessible False-blocked

    Methods:
        __init__(self, name: str = "TEST_1", map_data_directory: str = None):
            Initializes a Map instance with a specified name and data directory. Loads the map data from the
            corresponding file within the provided or default directory.
        load_map_data(self, path: str):
            Loads and parses map data from a specified file path. This method updates the map's attributes
            based on the contents of the file including the name, grid configuration, and paths.
        tile_accessibility(self, tile: Coord) -> bool:
            Checks if given tile is blocked or accessible to place tower.
    """

    def __init__(self, root_directory: str, name: str = "TEST_1") -> None:
        """
        Initializes a new instance of the Map class, loading map data from a specified file within a directory.

        This constructor sets up the map with a default or specified name and attempts to load its configuration
        from a data file that matches the map name in the provided or default directory. If the directory is not specified,
        it defaults to a 'maps' subdirectory located relative to this module's path. The initialization process involves
        parsing the map's metadata, grid data for accessibility, and paths if available.

        Arguments:
            name (str): The default name of the map if not specified otherwise, used to locate the corresponding map data file.
                        Defaults to "TEST_1", implying that the file "TEST_1_map.dat" should exist in the specified directory.
            root_directory (str): The root directory of the repository for relative path operations.
                                            If not provided, it defaults to a 'maps' directory relative to the location of this module's file.

        Raises:
            FileNotFoundError:  If the specified map data file does not exist in the provided directory, this will
                                inform the user about the missing file but does not stop the execution; instead,
                                it initializes the map with default or empty configurations.
        """
        map_data_directory = os.path.join(root_directory, "Assets", "gfx", "maps")

        file_path = os.path.join(map_data_directory, f"{name}.dat")

        self.name: str = name
        self.paths: tuple = ()
        self.grid: list = []

        self.load_map_data(file_path)

    def load_map_data(self, path: str) -> None:
        """
        Loads and parses the map data from a file.

        Arguments:
            path (str): The file path from which to load the map data.
        
        This method parses the map data file, updating the attributes of the map object
        based on the contents of the file. It reads the map's name, grid configuration, and enemies paths.
        """
        try:
            with open(path, 'r') as file:
                data = file.readlines()
        except FileNotFoundError:
            print(f"Map data file not found: {path}")

        for i, line in enumerate(data):
            line = line.strip()

            # Get name
            if line.startswith("Name:"):
                self.name = line.split("Name:", 1)[1].strip()

            # Get grid accesibility (whaether a tile is taken or accessible)
            elif line.startswith("Grid:"):
                # Parse through tiles starting 2 rows below (skipping "Grid:" row and "+--...--+" row)
                for line in data[i + 2:]:
                    # Stop reading grid at "+--..." row
                    if line[0] == '+':
                        break
                    row = [] # Temporary list for storing boolian representation of the row
                    # Iterate over characters in a row skipping spaces and initial "| "
                    for character in line[2::2]:
                        # Stop at vertical borer
                        if character == '|':
                            break
                        # Append True if the row is not taken
                        row.append(character == ' ')
                    # Append read row 
                    self.grid.append(row)

            # Get enemies paths
            elif line.startswith("Paths:"):
                temp_paths = [] # Temporary list for paths
                # Iterate over lines below "Paths:" every other line to skip path numeration
                for j, line in enumerate(data[i + 1:], i + 2):
                    # If current line is a path numerating one parse line below to read and convert the data within it
                    if line.startswith("Path"):
                        temp_path = []# Temporary list for currently read path
                        line = data[j].split(" > ") # split path into tile segments
                        # Append coordinates of each tile to the temp_path list
                        for element in line:
                            x, y = element.split(", ")
                            temp_path.append(Coord(int(x), int(y)))
                        # Append temp_path into temp_paths and convert it into inmutable type (tuple)
                        temp_paths.append(tuple(temp_path))
                # Convert list of paths into inmutable type (tuple)
                self.paths = tuple(temp_paths)

    def tile_accessibility(self, tile: Coord) -> bool:
        """
        Checks if given tile is blocked or accessible to place tower.
        
        Args:
            tile (Coord): Grid coordinates of a tile to check.

        Returns:
            Tile accessibility: True - accessible, False - blocked
        """
        return self.grid[tile.y][tile.x]

    def __str__(self) -> str:
        """Return a formatted string representation of the map data."""
        # Create a bordered grid presentation
        top_border = '+-' + '-' * (2 * len(self.grid[0])) + '+'
        bottom_border = top_border
        rows = ['| ' + ' '.join(' ' if tile else 'x' for tile in row) + ' |' for row in self.grid]
        
        # Convert the grid and path lists into strings
        grid_str = '\n'.join([top_border] + rows + [bottom_border])
        paths_str = '\n'.join([f"Path {i}:\n{' > '.join(map(str, path))}" for i, path in enumerate(self.paths) if path])

        return f"\nName: {self.name}\n\nGrid:\n{grid_str}\n\nPaths:\n{paths_str}\n"
