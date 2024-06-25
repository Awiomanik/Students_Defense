from Classes.Utilities import Coord
from Classes.Map.Map_Class import Map
from typing import Type, Self


class Enemy:
    """"
    Represents an enemy with specific properties: health and speed.

    Class Attributes:
    enemy_types (dict) : Dictionary defining an enemy with his health and speed.

    Instance Atributes:
    life (int): The current health of the enemy.
    speed (int): The speed at which the enemy moves.

    Methods:
    __init__(enemy_type : str = 'test_enemy'): Initializes an enemy with a specified type.
    __str__() -> str: Returns a string representation of the enemy, including its life and speed.
    """

    enemy_types = {'Marta' : {'hp': 3, 'speed': 5}}

    def __init__(self, enemy_type: str = 'test_enemy'):
        """
        Initializes the Enemy with the specified type.

        Arguments:
        enemy_type (str): The type of enemy to be created (default is 'test_enemy').
        """
        self.life: int = Enemy.enemy_types[enemy_type]['hp']
        self.speed: int = Enemy.enemy_types[enemy_type]['speed']
    
    def __str__(self):
        """
        Returns a string representation of the enemy.

        Returns:
            A string representing the enemy's life (health) and speed.
        """
        return f"Enemy(life={self.life}, speed={self.speed})"
    
    
class EnemyManager:
    """
    Manages enemies on the map, defining how the the moves along the created path,
    storing their current life and checking if the enemy has died.

    Class Attributes:
    present (list): A list that is storing all currently active enemies.

    Instance Attributes:
    name (str): The type of enemy being managed.
    map (Map): The game map on which the enemies will move.
    path (list): The path along which the enemies move.
    enemy_type (Enemy): The enemy instance being managed.
    speed (int): The speed of the enemy.
    life (int): The current health of the enemy.
    pos (Coord): The current position of the enemy on the map.
    display_pos (tuple): The display position of the enemy for UI.
    grid_pos (Coord): The grid position of the enemy on the map.
    tile (int): The current tile index in the path that the enemy is moving towards.
    hp_display: Placeholder for the enemy's health display in the UI.
    attacked (bool): Indicates if the enemy has been attacked.
    attacked_count (int or None): Counter for the attacked.
    damaged_player (bool): Indicates if the enemy has damaged the player.

    Methods:
    __init__(map: Map, enemy_type: str = 'test_enemy'): Initializes an enemy manager with a specified map and enemy type.
    __repr__() -> str: Returns a string representation of the enemy: type(name), health, and position.
    take_damage(damage): Reduces the enemy's life by the specified damage amount and sets it to attacked state if life is reduced.
    remove_attacked(): Decreases the attacked_count if the enemy is attacked and removes the attacked state when the count reaches zero.
    movement(): Moves the enemy along the defined path on the map based on its speed. If the enemy reaches the end of the path, it continues moving right.
    remove_enemy(): Removes the enemy from the present list if its life reaches zero.
    

    Class methods:
    reset(cls) -> None: Clears all enemies.
    endlevel():  method to clear all active enemies at the end of a level.
    update():  method to update all active enemies, checking their health, movement, and attacked state every frame.
    """

    present: list[Self] = []

    def __init__(self, map: Map, enemy_type: str = 'test_enemy'):
        """
        Initializes the EnemyManager with the specified map and enemy type.

        Arguments:
        map (Map): The game map on which the enemies will move.
        enemy_type (str): The type of enemy to be managed (default is 'test_enemy').
        """
        self.name: str = enemy_type
        self.map: Map = map
        self.path: list = map.paths[0]
        self.enemy_type: Enemy = Enemy(enemy_type)
        self.speed: int = self.enemy_type.speed
        self.life: int = self.enemy_type.life
        self.grid_pos: Coord = self.path[0]
        self.display_pos: tuple = tuple(Coord.grid_middle_point(self.grid_pos))
        self.pos: Coord = Coord(*self.display_pos)
        self.tile: int = 0
        self.hp_display: int = None # used in UI
        self.attacked: bool = False
        self.attacked_count: int = None
        self.damaged_player: bool = False
        EnemyManager.present.append(self)

    def __repr__(self) -> str:
        """
        Returns a string representation of the enemy.

        Returns:
        str: A string representing the enemy's name, health, and position.
        """
        return(f"{self.name} enemy with {self.life} hp and {self.pos} position")
    
    def take_damage(self, damage):
        """
        Reduces the enemy's life by the specified damage amount and sets it to attacked state.

        Arguments:
        damage (int): The amount of damage to expose the enemy.
        """

        self.life -= damage
        if self.life < 0:
            self.life = 0
        self.attacked = True
        self.attacked_count = 10

    def remove_attacked(self):
        """
        Decreaseas the attacked_count if the enemy is attacked and removes the attacked state
        when the count reaches zero.
        """

        if self.attacked_count:
            self.attacked_count -= 1
        else:
            self.attacked = False

    def movement(self):
        """
        Moves the enemy along the defined path on the map based on its speed. 
        If the enemy reaches the end of the path, it continues moving right.
        """

        if self.tile < len(self.path):
            destination: Coord = self.path[self.tile] 
            direction: Coord = destination - self.grid_pos
            self.pos += Coord(self.speed*direction.x,self.speed*direction.y)
            self.display_pos: tuple = (self.pos.x - 30,self.pos.y - 30)
            if (
                destination.grid_middle_point().x - self.speed < self.pos.x < destination.grid_middle_point().x + self.speed
            ) and (
                destination.grid_middle_point().y - self.speed < self.pos.y < destination.grid_middle_point().y + self.speed
            ):
                self.tile += 1
                self.grid_pos = Coord(self.pos.x//120,self.pos.y//120)
        else:
            self.pos += Coord(self.speed,0)
            self.display_pos: tuple = (self.pos.x - 30,self.pos.y - 30)
            if self.pos.x >= 1980 and not self.damaged_player:
                self.damaged_player = True
            if self.damaged_player == "done":
                EnemyManager.present.remove(self)
    
    @classmethod
    def reset(cls) -> None:
        """Clear all enemies, when new game starts."""
        cls.present = [] # clearing list
                
    def remove_enemy(self): 
        """Remove the enemy from the present list if its life reaches zero."""
        if self.life == 0:
            EnemyManager.present.remove(self)

    @classmethod
    def endlevel(cls):
        """Clear all active enemies at the end of a level."""
        cls.present = []

    @classmethod
    def update(cls : Type[Self]) -> None: 
        """
        Class method to update all active enemies, checking their health, movement, 
        and attacked state every frame.
        """
        for enemy in cls.present:
            enemy.remove_enemy()
            enemy.movement()
            enemy.remove_attacked()

## TEST ##
#x = 0
#test = EnemyManager()
#while len(EnemyManager.present):
#    x+=1
#   print('pixel position:',test.pos,'grid position:',test.grid_pos)
#    EnemyManager.update()
#    if x == 20000:
#        break