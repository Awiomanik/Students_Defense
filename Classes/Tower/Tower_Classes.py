
"""Tower meneger module"""

from ..Utilities import Coord
from ..Enemy.Enemy import Enemy, Enemy_Manager
from ..Level.Test_Level import Level
from math import ceil

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
#######################################################dmg##no of shots#####bounce#######cost######aoe range##################################projectile asset
##############################################range#########cd#######target######no of b.#####aoe#############tower asset##########################
    tower_types = {"test_tower_1"                 : (300, 1, 60  ,  1, True , False, None, 1 ,  True,   100, 'tower_placeholder.png'            , 'bullet_placeholder.png'),
                   "test_tower_2"                 : (180, 2, 60  ,  1, True ,  True,    2, 1 , False,  None, 'tower_placeholder.png'            , 'bullet_placeholder.png'),
                   "Algebra_basic"                : (400, 2, 120 ,  1, True , False, None, 10, False,  None, 'Algebra_basic.png'                , 'Algebra_projectile.png'),
                   "Algebra_LT"                   : (300, 4, 90  ,  1, True ,  True,    4, 50, False,  None, 'Algebra_LT_specialist.png'        , 'Algebra_projectile.png'),
                   "Algebra_complex_"             : (400, 2, 60  , 12, False, False, None, 50, False,  None, 'Algebra_complex_specialist.png'   , 'Algebra_projectile.png'),
                   "Analysis_basic"               : (300, 1, 45   , 1, True,  False, None, 10, False,  None, 'Analysis_basic.png'               , 'Analysis_projectile.png'),
                   "Analysis_calculus_specialist" : (300, 2, 45   , 1, True,  False, None, 50,  True,    50, 'Analysis_calculus_specialist.png' , 'Analysis_projectile.png'),
                   "Analytic_functions_specialist": (300, 2, 15   , 1, True,  False, None, 50, False,  None, 'Analytic_functions_specialist.png', 'Analysis_projectile.png'),
                   "Programming_basic"            : (300, 1, 120  , 1, True,  False, None, 10,  True,    50, 'Programming_basic.png'            , 'Programming_projectile.png'),
                   "Programming_object"           : (300, 4, 90   , 1, True,  False, None, 50,  True,   100, 'Programming_object.png'           , 'Programming_projectile.png'),
                   "Programing_spaghetti_decoder" : (300, 1, 30   , 1, True,   True,    8, 60, False,  None, 'Programming_spaghetti_decoder.png', 'Spaghetti_projectile.png')
                   }
    """
        Tower stats positions:
        0 - range
        1 - damage
        2 - cooldown
        3 - number of shots
        4 - targeting
        5 - bouncing
        6 - number of bounces
        7 - tower cost
        8 - aoe?
        9 - aoe range
        10 - tower asset
        11 - projectile asset
    """
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
        self.bouncing_count, \
        self.cost, \
        self.aoe, \
        self.aoe_range, \
        self.tower_asset, \
        self.projectile_asset \
            = Tower.tower_types[tower_type]
        self.base_cooldown = Tower.tower_types[tower_type][2]
        self.tower_name = tower_type

    def cooldown(self):
        """Decreases the attack cooldown by one frame."""
        self.atk -= 1
        self.atk -=1

    def setbasecooldown(self):
        """Resets the attack cooldown to the base cooldown value."""
        self.atk = self.base_cooldown

class Projectiles:
    displayed : list['Projectiles']= []
    def __init__(self,start : Coord, finish : Coord, asset : str, speed : int = 80):
        self.asset = asset
        self.start = start
        self.pos = start
        self.destination = finish
        self.speed = speed
        self.display_pos = self.pos - 15
        self.mov_vector = None
        self.vector_len = None
        self.travelled = 0
        Projectiles.displayed.append(self)
    def display_update(self):
        self.display_pos = self.pos - 15
    def create_vector(self):
        base_vector = Coord(self.start.x - self.destination.x,self.start.y - self.destination.y)
        self.vector_len = (base_vector.x**2 + base_vector.y**2)**0.5
        normalized_vector = Coord(base_vector.x/self.vector_len,base_vector.y/self.vector_len)
        self.mov_vector = Coord(normalized_vector.x*self.speed,normalized_vector.y*self.speed)
    def animation (self):
        self.pos += self.mov_vector
        self.pos.x = ceil(self.pos.x)
        self.pos.y = ceil(self.pos.y)
        self.travelled += self.speed
        self.display_update()
    def remove(self):
        Projectiles.displayed.remove(self)
    @classmethod
    def animate_all(cls):
        for projectile in cls.displayed:
            projectile.animation()

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
    enemies : list['Enemy_Manager'] = Enemy_Manager.present


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
        self.own_projectile = None
        self.target_criteria = 'low_hp'
        if self.tower_type.bouncing:
            self.remaining_bounces = self.tower_type.bouncing_count
            self.distance : list[(int,Enemy_Manager)] = []
            self.already_attacked = None
        Tower_Manager.towers.append(self)
    #def projectile(self,enemy_position : Coord,projectile_pos : Coord):
    #    attack_vector : Coord = enemy_position - self.pos
    #    attack_vector20 = Coord(20*attack_vector.x/((attack_vector.x**2 + attack_vector.y**2)**0.5),20*attack_vector.y/((attack_vector.x**2 + attack_vector.y**2)**0.5))
    #    proj_pos : Coord = self.pos 
    #    return proj_pos

    def untargetted_attack(self):
        """Manages untargetted attacks"""

    def attack(self):
        """Manages attacks, targeting the weakest enemy within range if the tower is ready to fire."""
        criteria = self.target_criteria

        if self.tower_type.atk !=0:#Passing time between attacks
            self.tower_type.cooldown()
            if self.tower_type.bouncing:
                if self.remaining_bounces:
                    if self.own_projectile.travelled > self.own_projectile.vector_len:
                        self.own_projectile.remove()
                        for possible_target in self.distance:
                            if possible_target[0] <= 100 and possible_target[1] not in self.already_attacked:
                                self.already_attacked.append(possible_target[1])
                                next_target : Enemy_Manager  = possible_target[1]
                                next_target.take_damage(self.tower_type.dmg)
                                self.distance.clear()
                                break
                            self.tower_type.setbasecooldown()
                            break
                else:
                    self.already_attacked.clear()
        else:#if tower is ready to fire, it will look for enemies in range
            if self.tower_type.bouncing:
                self.remaining_bounces = self.tower_type.bouncing_count
            inrange : dict[Enemy_Manager, Enemy.life]= {}#this dict will contain enemies in range as keys and their hp as values
            self.inrange = inrange
            for enemy in Tower_Manager.enemies:
                distance = ((enemy.pos.x - self.pos.x)**2 + (enemy.pos.y - self.pos.y)**2)**0.5#calculates distance between tower and enemy
                if distance <= self.tower_type.range: #lists enemies within range (idea: we could use non-carthesian spaces)$$ #############coord class required###########
                    inrange[enemy] = (enemy.life)
            if not len(inrange):# returns when list length is 0
                return

        ################################every frame, UI should 
            for enemy in inrange.keys():
                if criteria == 'low_hp':
                    value = self.inrange[enemy]
                    condition = min(inrange.values())
                elif criteria == 'high_hp':
                    value = self.inrange[enemy]
                    condition = max(inrange.values())
                """
                elif criteria == 'front':
                    value = self.inrange[enemy][1]
                    condition = max(inrange.values()[1])
                elif criteria == 'back':
                    value = self.inrange[enemy][1]
                    condition = min(inrange.values()[1])
                """
                if value == condition: #defaults to attacking weakest enemies, might be choose-able later.$$
                    target = enemy
                    if self.tower_type.aoe: #checks if the tower has aoe damage and which enemies are in range of it
                        for victims in self.enemies:
                            area = ((victims.pos.x - target.pos.x)**2 + (victims.pos.y - target.pos.y)**2)**0.5
                            if area <= self.tower_type.aoe_range:
                                victims.take_damage(self.tower_type.dmg)
                        self.tower_type.setbasecooldown()
                        break
                    elif self.tower_type.bouncing:
                        next_target = target
                        target.take_damage(self.tower_type.dmg)
                        self.own_projectile = Projectiles(self.pos,target.pos,self.tower_type.projectile_asset)
                        self.own_projectile.create_vector
                        self.already_attacked = [next_target]
                        for bounce in range(self.tower_type.bouncing_count):
                            self.distance = []
                            for victim in self.enemies:
                                area = ((victim.pos.x - next_target.pos.x)**2 + (victim.pos.y - next_target.pos.y)**2)**0.5
                                self.distance.append((area, victim))
                            self.distance.sort()
                        self.tower_type.setbasecooldown()
                        break
                    else:
                        target.take_damage(self.tower_type.dmg)
                        self.tower_type.setbasecooldown()
                        break
                        #projectile = Projectiles(self.pos, enemy.pos)

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
            if tower.tower_type.aoe:
                tower.attack()
            else:
                tower.untargetted_attack()

    @classmethod
    def reset(cls):
        """Clears all towers, when new game starts"""
        cls.towers = [] # clearing list
        
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