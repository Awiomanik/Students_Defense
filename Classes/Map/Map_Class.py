"""Map class for storing map information"""

# IMPORTS
from ..Utilities import Coord
import os

class Map():
    """
    """

    def __init__(self, name : str = "TEST_1", map_data_directory : str = None) -> None:
        """
        """
        # Set directory if not given
        if map_data_directory is None:
            map_data_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps")

        # Combain the file path
        file_path = os.path.join(map_data_directory, f"{name}_map.dat")

        # Initialize atributes
        self.name = name # temporary name (stays if "Name: xyz" not found in the file)
        self.paths = ()
        self.grid = []

        # Parse the data
        self.load_map_data(file_path)

    def load_map_data(self, path : str) -> None:
        try:
            with open(path, 'r') as file:
                data = file.readlines()

            # Parse each line
            for i, line in enumerate(data):
                line = line.strip()

                if line.startswith("Name:"):
                    self.name = line.split("Name:", 1)[1].strip()

                elif line.startswith("Grid:"):
                    for line in data[i + 2:]:
                        if line[0] == '+':
                            break
                        row = []
                        for character in line[1:]:
                            if character == '|':
                                break
                            row.append(character == ' ')
                        self.grid.append(row)

                elif line.startswith("Paths:"):
                    temp_paths = []
                    for j, line in enumerate(data[i + 1:], i + 2):
                        if line.startswith("Path"):
                            temp_path = []
                            line = data[j].split(" > ")
                            for element in line:
                                x, y = element.split(", ")
                                temp_path.append(Coord(x, y))
                            temp_paths.append(tuple(temp_path))
                    self.paths = tuple(temp_paths)

            print(self.name)
            for g in self.grid:
                for h in g:
                    print('x' if h else ' ', end='')
                print()
            print(self.paths)
                            



        except FileNotFoundError:
            print(f"Map data file not found: {path}")



if __name__ == "__main__":
    Map()