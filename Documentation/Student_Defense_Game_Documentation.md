### Student Defense Game Documentation

#### 1. Game Startup Instructions

##### 1.1 Required Libraries
To run the game, the following libraries need to be installed:
- `pygame`
- `os`

Installation command:
```bash
pip install pygame
```

##### 1.2 Running the Prototype
1. After launching the game, an intro will appear on the screen.
2. Next, the main menu will appear, where the player can choose to start the game or exit.
3. Upon selecting to start the game, the player enters the actual gameplay.
4. During gameplay, the player can buy and build towers to defend their position against incoming waves of enemies.

#### 2. User Guide

##### 2.1 Class `Level`
- **Methods:**
  - `__init__(self, level_number: int)`: Initializes a level with the given number.
  - `add_wave(self, enemy_type: enm.Enemy, quantity: int, interval: int)`: Adds a wave of enemies.
  - `get_waves(self) -> List[Dict[str, Tuple[int, int]]]`: Returns a list of enemy waves.
  - `start_level(self)`: Starts the level, displaying information about enemy waves.

##### 2.2 Class `Map`
- **Methods:**
  - `__init__(self, name: str = "TEST_1", map_data_directory: str = None)`: Initializes a map based on map data file.
  - `load_map_data(self, path: str)`: Loads map data from a file.

##### 2.3 Class `Tower`
- **Methods:**
  - `__init__(self, range: int, damage: int, atk_speed: int, shot_count: int, targeting: bool, bouncing: bool, own_asset, shot_asset)`: Initializes a tower with specified parameters.

##### 2.4 Class `Tower_Manager`
- **Methods:**
  - `__init__(self, tower_type: Tower, coord, enemies)`: Initializes tower manager for a given tower type, coordinates, and enemies.
  - `reset(cls)`: Resets the tower list.
  - `attack(self)`: Executes tower attack on enemies within range.

##### 2.5 Class `Enemy`
- **Methods:**
 - `__init__(self, life: int, speed: int, image, position: Tuple[int, int], destination: Tuple[int, int])`: Initializes an enemy with specified parameters.
 - `calculate_direction(self) -> Tuple[float, float]`: Calculates the enemy's movement direction based on its position and destination.
 - `move(self)`: Moves the enemy towards its destination.
 - `update(self)`: Updates the enemy's state (e.g., performs movement).
 - `__str__(self) -> str`: Returns a string representation of the enemy.

##### 2.6 Class `Game`
- **Methods:**
  - `__init__(self, display_intro: bool = True) -> None`: Initializes a game instance.
  - `run_game_loop(self) -> None`: Starts the main game loop.
  - `__main__()`: Function to launch the game.

#### 3. Planned UML Class Diagram

The class diagram illustrates dependencies between classes, as well as their attributes and methods:

----------------------------------------
|                Game                  |
----------------------------------------
| - ui: UI                             |
| - towers: TowerManager               |
| - player: Player                     |
| - level: Level                       |
----------------------------------------
| + __init__(display_intro: bool)      |
----------------------------------------
               |
               |
               |
               |
               |
               v
----------------------------------------
|                 UI                   |
----------------------------------------
| - screen: pygame.Surface             |
| - clock: pygame.time.Clock           |
| - mouse_click: bool                  |
| - pos: Tuple[int, int]               |
| - gfx_path: str                      |
----------------------------------------
| + intro()                            |
| + main_menu() -> bool                |
| + load_lvl(map_name: str,            |
|            towers_names: Dict[str,   |
|                         str],        |
|            bullets_names: Dict[str,  |
|                            str]) ->  |
|            None                      |
| + update()                           |
----------------------------------------
               |
               |
               |
               |
               |
               v
----------------------------------------
|             TowerManager             |
----------------------------------------
| - towers: List[Tower]                |
----------------------------------------
| + reset()                            |
----------------------------------------
               |
               |
               |
               |
               |
               v
----------------------------------------
|               Player                 |
----------------------------------------
| - name: str                          |
| - gold: int                          |
| - tower_manager: TowerManager        |
| - placed_towers: List[Tower]         |
----------------------------------------
| + can_afford_tower(tower: Tower) ->  |
|   bool                               |
| + place_tower(tower: Tower, x: int,  |
|   y: int) -> bool                    |
----------------------------------------
               |
               |
               |
               |
               |
               v
----------------------------------------
|                Level                 |
----------------------------------------
| - level_number: int                  |
| - enemy_waves: List[Dict[str,        |
|                   Tuple[int, int]]]  |
----------------------------------------
| + add_wave(enemy_type: Enemy,        |
|            quantity: int,            |
|            interval: int) -> None    |
| + start_level() -> None              |
----------------------------------------
               |
               |
               |
               |
               |
               v
----------------------------------------
|                Map                   |
----------------------------------------
| - name: str                          |
| - paths: Tuple[Tuple[Coord]]         |
| - grid: List[List[bool]]             |
----------------------------------------
| + __init__(name: str,                |
|             map_data_directory: str) |
| + load_map_data(path: str) -> None   |
| + __str__() -> str                   |
----------------------------------------
               |
               |
               |
               |
               |
               v
----------------------------------------
|                Enemy                 |
----------------------------------------
| - life: int                          |
| - speed: int                         |
| - image                              |
| - x: int                             |
| - y: int                             |
| - position                           |
| - destination                        |
| - direction                          |
----------------------------------------
| + __init__(life: int,                |
|            speed: int,               |
|            image,                    |
|            position,                 |
|            destination)              |
| + calculate_direction() -> Tuple[int,|
|                                int]  |
| + move() -> None                     |
| + update() -> None                   |
| + __str__() -> str                   |
----------------------------------------

#### 4. Updated Action Plan for Subsequent Weeks of Work
- Implementing basic game mechanics, including UI drawing, enemy movement, and tower attacks.
- Adding advanced features such as different enemy and tower types, and more complex pathfinding.
- Testing and optimizing code to ensure smooth and error-free gameplay.

#### 5. Updated Feature Plan for the Completed Application

- **Basic Features:**
  - Adding enemy waves.
  - Managing towers and attacking enemies.
  - Loading and displaying maps.

- **Advanced Features:**
  - Various types of towers and enemies.
  - Special tower abilities.
  - Different difficulty levels and diverse maps.
  - Integration with scoring and ranking system.

- **User Interface:**
  - Intuitive interface for managing the game.
  - Health, point, and resource indicators.