"""Tower meneger module"""

from ..Utilities import Coord
from ..Level import Test_Level
from ..Enemy import Enemy

class Tower: #defining properties of towers
    tower_types = {"test_tower_1" : (300, 1, 120, 1, True, 0, 1),
                   "test_tower_2" : (180, 1, 120, 2, True, 0, 1)}
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
    towers = []

    def __init__(self,
                 tower_type_str : str = "test_tower", 
                 pos : Coord = Coord(0, 0),
                 enemies : list = None): #Enemy_Manager.present) -> None:
        "Place tower"
        self.tower_type = Tower(tower_type_str)
        self.pos = pos
        self.enemies = enemies
        Tower_Manager.towers.append(self)

    def attack(self):
        """Method takes care of everything related to attacks - manages cooldowns and attacks weakest enemy if any is in range"""
        if self.tower_type.atk !=0:#Passing time between attacks
            self.tower_type.cooldown()
        else:#if tower is ready to fire, it will look for enemies in range
            inrange = {}#this dict will contain enemies in range as keys and their hp as values
            for enemy in self.enemies:
                distance = ((enemy.pos.x-self.pos.x)**2 + (enemy.pos.x-self.pos.y)**2)**0.5#calculates distance between tower and enemy
                if distance <= self.tower_type.range: #lists enemies within range (idea: we could use non-carthesian spaces)$$ #############coord class required###########
                    inrange[enemy] = distance
            if len(inrange):#returns false when list length is 0
                return
            for enemy in inrange.keys:
                if inrange[enemy] == min(inrange.values): #defaults to attacking weakest enemies, might be choose-able later.$$
                    #attack_vector = enemy_coord.sub(self.coord)############################################## attack animation in pygame ####################################################################### at the moment doesnt account for enemy movement. it moves fast tho
                    #attack_vector20 = coord(20*attack_vector.x/((attack_vector.x**2 + attack.vector.y**2)**0.5),20*attack_vector.y/((attack_vector.x**2 + attack.vector.y**2)**0.5)) ### projectile will travel 20 pixels per frame
                    #proj_coord = self.coord
                    #distance_traveled = 0
                    #distance_to_travel = ((proj_coord.x - self.coord.x)**2 + (proj_coord.y - self.coord.y)**2)**0.5
                    #atk_png = pygame.image.load(self.tower_type.s_asset)
                    #while distance_traveled<distance_to_travel:
                        #display.blit(atk_png,self.coo) ################################## display !!!####
                        #proj_coord.add(attack_vector20)
                        #distance_traveled = ((proj_coord.x - self.coord.x)**2 + (proj_coord.y - self.coord.y)**2)**0.5
                    #self.enemies[enemy].take_damage(self.tower_type.dmg)
                    self.tower_type.setbasecooldown()

    @classmethod
    def frame(cls):
        """Method intended to be executed every frame in order to execute all towers' attacks"""
        for tower in cls.towers:
            tower.attack()
    @classmethod
    def reset(cls):
        """Methot needed to clear all towers, supposedly when new game starts"""
        cls.towers = [] #clearing list