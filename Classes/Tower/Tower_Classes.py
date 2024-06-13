
"""Tower meneger module"""

from ..Utilities import Coord
from ..Enemy.Enemy import Enemy, Enemy_Manager
from ..Level.Test_Level import Level

class Tower: #defining properties of towers
    tower_types = {"test_tower_1" : (300, 1, 60, 1, True, 0, 1),
                   "test_tower_2" : (180, 2, 60, 1, True, 0, 1)}
    def __init__(self, tower_type : str = "test_tower") -> None:
        """
        Initializes tower of type tower_type.
        Types of towers are to be defined in dictionary located in another file. This dictionary is called tower_types. 
        tower_types elements are constructed as follows:
        tower_type : {range : int, damage : int, base_cooldown : int, shot_count : int, targeting : bool, bouncing : int}
        These mean:
        range - Tower's attack range represented in pixels
        damage - damage tower deals when enemy is attacked
        base_cooldown - time between subsequent attacks represented in frames
        shot_count - number of projectiles fired
        targeting - defines if tower attacks defined enemy, or fires projectiles in defined directions. The latter are to be detailed in later stages of development.
        bouncing - defines if after first attack projectiles will bounce towards other nearby enemies.
        cost - cost of tower

        """

        # Initialize tower
        self.range, \
        self.dmg, \
        self.atk, \
        self.shot_count, \
        self.targeting, \
        self.bouncing, \
        self.cost \
            = Tower.tower_types[tower_type]
        self.base_cooldown = Tower.tower_types[tower_type][2]
    def cooldown(self):
        self.atk -=1
    def setbasecooldown(self):
        self.atk = self.base_cooldown

class Tower_Manager:
    """This class is responsible for storing information about towers and attacking enemies"""
    towers : list['Tower_Manager'] = []
    enemies : list['Enemy'] = Enemy_Manager.present
    def __init__(self,
                 tower_type_str : str = "test_tower", 
                 pos : Coord = Coord(0, 0)) -> None:
        "Place tower"
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
        """Method takes care of everything related to attacks - manages cooldowns and attacks weakest enemy if any is in range"""
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
                    enemy.take_damage(self.tower_type.dmg)
                    self.tower_type.setbasecooldown()
                    break

    #def upgrade(self,
    #            tower_type_str : str = "test_tower"):
    #    self.tower_type = Tower(f"{tower_type_str}_upgrade")                    

    @classmethod
    def update(cls):
        """Method intended to be executed every frame in order to execute all towers' attacks"""
        cls.enemies = Enemy_Manager.present #update enemy list
        for tower in cls.towers:
            tower.attack()
    @classmethod
    def reset(cls):
        """Methot needed to clear all towers, supposedly when new game starts"""
        cls.towers = [] #clearing list
        
    def load_lvl():
        # Clear any old data
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