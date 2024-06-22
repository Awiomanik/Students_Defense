
"""Tower meneger module"""

from ..Utilities import Coord
from ..Enemy.Enemy import Enemy, Enemy_Manager
from ..Level.Test_Level import Level

class Tower: 
    """Defining properties of towers.
        
        Class Attibutes:
        tower_types (dict): A class-level dictionary defining different types of towers and their properties.


        Instance Attributes:
        range (int): The tower's attack range in pixels.
        
        dmg (int): The damage the tower deals when attacking an enemy.
        
        atk (int): The time between subsequent attacks in frames.
        
        shot_count (int): The number of projectiles fired by the tower.
        
        targeting (bool): Indicates if the tower targets a specific enemy or fires projectiles in defined directions.
        
        bouncing (int): Indicates if the projectiles will bounce towards other nearby enemies after the initial attack.
        
        cost (int): The cost of the tower.
        
        base_cooldown (int): The base cooldown time between attacks.

        Methods:
        __init__(tower_type: str = "test_tower") -> None:
            Initializes a tower with the specified type.
        
        cooldown():
            Decrements the attack cooldown by one frame.
        
        setbasecooldown():
            Resets the attack cooldown to the base cooldown value
        """
    

    tower_types = {"test_tower_1" : (300, 1, 60, 1, True, 0, 1, True, 100),
                   "test_tower_2" : (180, 2, 60, 1, True, 0, 1, False, None)}
    
    def __init__(self, tower_type : str = "test_tower") -> None:
        """
        Initializes a tower with the specified type.

        Arguments:
        tower_type : str
            The type of tower to be created (default is "test_tower").
        """
        self.range, \
        self.dmg, \
        self.atk, \
        self.shot_count, \
        self.targeting, \
        self.bouncing, \
        self.cost, \
        self.aoe, \
        self.aoe_range \
            = Tower.tower_types[tower_type]
        self.base_cooldown = Tower.tower_types[tower_type][2]

    def cooldown(self):
        """Decreases the attack cooldown by one frame."""
        self.atk -= 1
        self.atk -=1

    def setbasecooldown(self):
        """Resets the attack cooldown to the base cooldown value."""
        self.atk = self.base_cooldown

class Tower_Manager:
    """
    Manages tower instances, handling their placement, attacks, and interactions with enemies.

    Class Attributes:
    towers (list['Tower_Manager']): attribute storing all currently placed towers.
    
    enemies (list['Enemy']): attribute referencing the list of active enemies from the Enemy_Manager class.
    
    Attributes:
    tower_type (Tower): The tower instance being managed.
    
    pos (Coord): The position of the tower on the map.
    
    display_pos (tuple): The display position of the tower for UI purposes.

    Methods:
    __init__(tower_type_str: str = "test_tower", pos: Coord = Coord(0, 0)) -> None:
        Initializes a tower at the specified position with the specified type.

    attack():
        Manages the tower's attacks, targeting the weakest enemy within range if the tower is ready to fire.
    
    Class methods:
    update():
        Updates all active towers, managing their attacks every frame.
    
    reset():
        Clears all towers, typically used when starting a new game.
    """

    towers : list['Tower_Manager'] = []
    enemies : list['Enemy'] = Enemy_Manager.present


    def __init__(self,
                 tower_type_str : str = "test_tower", 
                 pos : Coord = Coord(0, 0)) -> None:
        """
        Initializes a tower at the specified position with the specified type.

        Arguments:
        tower_type_str : str
            The type of tower to be created (default is "test_tower").
        pos : Coord
            The position to place the tower on the map.
        """
        self.tower_type = Tower(tower_type_str)
        self.pos = Coord((pos.x//120)*120,(pos.y//120)*120) + 60
        self.display_pos = (self.pos.x - 60,self.pos.y-60)
        Tower_Manager.towers.append(self)
    #def projectile(self,enemy_position : Coord,projectile_pos : Coord):
    #    attack_vector : Coord = enemy_position - self.pos
    #    attack_vector20 = Coord(20*attack_vector.x/((attack_vector.x**2 + attack_vector.y**2)**0.5),20*attack_vector.y/((attack_vector.x**2 + attack_vector.y**2)**0.5))
    #    proj_pos : Coord = self.pos 
    #    return proj_pos


    def attack(self):
        """Manages attacks, targeting the weakest enemy within range if the tower is ready to fire."""
        if self.tower_type.atk !=0:#Passing time between attacks
            self.tower_type.cooldown()
        else:#if tower is ready to fire, it will look for enemies in range
            inrange : dict[Enemy,Enemy.life]= {}#this dict will contain enemies in range as keys and their hp as values
            self.inrange = inrange
            for enemy in Tower_Manager.enemies:
                distance = ((enemy.pos.x - self.pos.x)**2 + (enemy.pos.y - self.pos.y)**2)**0.5#calculates distance between tower and enemy
                if distance <= self.tower_type.range: #lists enemies within range (idea: we could use non-carthesian spaces)$$ #############coord class required###########
                    inrange[enemy] = enemy.life
            if not len(inrange):#returns when list length is 0
                return
            for enemy in inrange.keys():
                if inrange[enemy] == min(inrange.values()): #defaults to attacking weakest enemies, might be choose-able later.$$
                    target = enemy
                    if self.tower_type.aoe: #checks if the tower has aoe damage and which enemies are in range of it
                        for victims in self.enemies:
                            area = ((victims.pos.x - target.pos.x)**2 + (victims.pos.y - target.pos.y)**2)**0.5
                            if area <= self.tower_type.aoe_range:
                                enemy.take_damage(self.tower_type.dmg)
                    else:
                        enemy.take_damage(self.tower_type.dmg)
                    self.tower_type.setbasecooldown()
                    break

    def upgrade(self, tier: int, tower_name: str):
        """This method upgrades a chosen tower""" 
        position = self.pos
        Tower_Manager.towers.remove(self) 
        if tier == 1:
          self.pos = position
          self.tower_type = Tower(f'{tower_name}_tier_2')
          self.display_pos = (self.pos.x - 60,self.pos.y-60)
          Tower_Manager.towers.append(self)    
        elif tier == 2:
          self.pos = position
          self.tower_type = Tower(f'{tower_name}_tier_3')
          self.display_pos = (self.pos.x - 60,self.pos.y-60)
          Tower_Manager.towers.append(self) 

    @classmethod
    def update(cls):
        """Updates all active towers, managing their attacks every frame."""
        cls.enemies = Enemy_Manager.present #update enemy list
        for tower in cls.towers:
            tower.attack()

    @classmethod
    def reset(cls):
        """Clears all towers, when new game starts"""
        cls.towers = [] #clearing list
        
    def load_lvl():
        """Clears old data and resets towers, used when loading a new level."""
        Tower_Manager.reset()

        
#level = Level(1)
##tower = Tower_Manager('test_tower_1')
#level.update()
#x = 0
#while level.enemies:
 #   print(level.enemies)
##    level.update
#    if tower.debug:
#        print(tower.debug)