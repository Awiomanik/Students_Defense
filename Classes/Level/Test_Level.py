"""
This module manages level data and enemy spawning for the Students Defense Game project.

Classes:
    Level - Handles level data, enemy spawning, and wave progression within a game level.
"""

from ..Enemy.Enemy import Enemy_Manager
import os
from ..Map import Map_Class

class Level:
    """
    Handles level data, enemy spawning, and wave progression within a game level.

    Class attributes:
        enemies (list[Enemy_Manager]): List of current enemies present in the level.
    
    Instance atributes:
        gold (int): The initial gold amount for the player in that level.
        lives (int): The number of lives the player starts with.
        waves_num (int): The number of waves in the level.
        waves (list[dict[str, int]]): The list of enemy waves, each wave represented by a dictionary of enemy types and their quantities.
        map (Map_Class.Map): The map object instance representing and menaging map data of the current level.
        current_wave (int): The index of the current wave.
        spawn_cooldown (int): The cooldown period between enemy spawns.
        current_wave_def (dict[str, int]): The current wave definition.
        current_enemy (str): The type of the current enemy being spawned.
        remaining_enemies (int): The total number of remaining enemies in the current wave.

    Methods:
        __init__(level_number: int, root_directory: str): Loads level data from file and initializes level attributes.
        spawn_enemy(): Spawns enemies based on the wave definitions and spawn cooldown.
        update(): Updates the level state by spawning enemies and managing enemy behavior.
        new_wave(): Advances to the next wave and updates wave-related attributes.
        def reset(cls) -> None: Clears all enemies.
    """

    # Class atributes
    enemies : list[Enemy_Manager] = Enemy_Manager.present

    # Methods
    def __init__(self, level_number : int, root_directory : str) -> None:
        """
        Loads level data from file and initializes level attributes.

        Args:
            level_number (int): The number of the level to load.
            root_directory (str): The root directory of the repository for relative path operations.
        """
        # Open data file and read it
        path = os.path.join(root_directory, "Assets", "lvl_data", f"lvl_{level_number}.dat")
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
        self.current_wave = 0
        self.spawn_cooldown = 0

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
                self.map = Map_Class.Map(root_directory, map_name)
            # Available_towers
            elif line.startswith("Available_towers:"):
                self.available_towers : list[str] = \
                    [tower.strip() for tower in line.split("Available_towers:")[1].split(',')]
                
        # Set new waves if waves data found in file
        if temp_waves:
            self.waves = tuple(temp_waves)

        # Set number of waves
        self.waves_num = len(self.waves)
        self.current_wave_def = self.waves[self.current_wave]
        self.current_enemy = list(self.current_wave_def.keys())[0]
        self.remaining_enemies = sum(self.current_wave_def.values())

    def spawn_enemy(self) -> None:
        """
        Spawns enemies based on the wave definitions and spawn cooldown.

        Returns:
            Enemy_Manager: The spawned enemy instance, if an enemy is spawned; otherwise, None.
        """
        if not self.remaining_enemies:
            pass
        elif self.spawn_cooldown == 0:
            spawned_enemy = Enemy_Manager(self.map, self.current_enemy) # despite not being further utilised, spawned_enemy is followed by Tower_Manager.present class attribute
            self.current_wave_def[self.current_enemy] -= 1
            self.spawn_cooldown = 60
            self.remaining_enemies = sum(self.current_wave_def.values())
            if self.current_wave_def[self.current_enemy] == 0:
                del self.waves[self.current_wave][self.current_enemy]
            return spawned_enemy
        else:
            self.spawn_cooldown -= 1

    def update(self):
        """
        Updates the level state by spawning enemies and managing enemy behavior.

        This method should be called every frame to process enemy spawning, movement, 
        attacks, and checking and updating player lives.
        """
        self.spawn_enemy()
        Enemy_Manager.update()
        for enemy in self.enemies:
            if enemy.damaged_player:
                self.lives -=1
                enemy.damaged_player = "done"
                
    def new_wave(self) -> None:
        """
        Advances to the next wave and updates wave-related attributes.

        This method increments the current wave index, sets the new wave definition,
        and resets the enemy-related attributes for the new wave.
        """
        self.current_wave += 1
        self.current_wave_def = self.waves[self.current_wave]
        self.current_enemy = list(self.current_wave_def.keys())[0]
        self.remaining_enemies = sum(self.current_wave_def.values())

    @classmethod
    def reset(cls) -> None:
        """Clears all enemies"""
        cls.enemies.clear()

        

# Use example:
#if __name__ == "__main__":

    #level1 = Level(level_number=1)
    #level1.add_wave(enemy_type=student, quantity=10, interval=5)
    #level1.start_level()
#

#A = Level(1)
#x = 0
#print('cooldown',A.spawn_cooldown)
#while A.remaining_enemies:
#    if x == 0:
#        print('remaining enemies',A.current_wave_def)
#        print('current enemy:',A.current_enemy)
#        print('cooldown',A.spawn_cooldown)
#        print('number of remaining enemies:',A.remaining_enemies)
#    if A.remaining_enemies:
#        A.spawn_enemy()
#        Enemy_Manager.update()
#        #print(A.spawn_cooldown)
#        print(Enemy_Manager.present)
#    if not A.spawn_cooldown or x == 0 or not A.remaining_enemies:
#        print('remaining enemies',A.current_wave_def)
#        print('current enemy:',A.current_enemy)
#        print('cooldown',A.spawn_cooldown)
#        print('number of remaining enemies:',A.remaining_enemies)
#    x += 1
#    if x == 20000:
#        print('cos nie tak')
#        break