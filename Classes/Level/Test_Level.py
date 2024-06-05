from typing import List, Dict, Tuple
import Classes.Enemy as enm
import os
from ..Map import Map_Class

class Level:
    def __init__(self, level_number : int, level_data_directory : str = None) -> None:
        """Loads level data from file"""
        # Set level data directory if no directory given
        if level_data_directory is None:
            level_data_directory = os.path.dirname(os.path.abspath(__file__))

        # Open data file and read it
        path = os.path.join(level_data_directory, f"lvl_{level_number}.dat")
        try:
            with open(path, 'r') as level_data:
                level_data = level_data.readlines()
        except FileNotFoundError:
            print(f"Level data file not found: {path}")

        # Set default atibutes
        self.gold : int = 0
        self.lives : int = 1
        self.waves_num : int = 1
        self.waves : list[dict[str, int]]= ({"test_enemy" : 1})
        temp_waves = []
        self.map = None

        # Parse level data to set atributes
        for line in level_data:
            line.strip()
            # Gold
            if line.startswith("Gold"):
                self.gold = int(line.split("Gold:", 1)[1].strip())
            # Lives
            elif line.startswith("Lives"):
                self.lives = int(line.split("Lives:", 1)[1].strip())
            # Waves
            elif line.startswith("Wave "):
                wave : list[tuple[str, str]] = [enemies.split('-') for enemies in line.split(':', 1)[1].split(',')]
                temp_waves.append({key.strip() : int(element.strip()) for element, key in wave})
            # Map
            elif line.startswith("Map"):
                map_name = line.split("Map:", 1)[1].strip()
                self.map = Map_Class.Map(map_name)
            # Available_towers
            elif line.startswith("Available_towers:"):
                self.available_towers : list[str] = [tower.strip() for tower in line.split(',')]
                
        # Set new waves if waves data found in file
        if temp_waves:
            self.waves = tuple(temp_waves)

        # Set number of waves
        self.waves_num = len(self.waves)

# Use example:
if __name__ == "__main__":

    level1 = Level(level_number=1)
    level1.add_wave(enemy_type=student, quantity=10, interval=5)
    level1.start_level()

