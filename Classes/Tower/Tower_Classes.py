from ..Utilities import Coord
from ..Enemy.Enemy import Enemy, EnemyManager
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
######################################################## dmg #no of shots## bounce #### cost #######aoe range######################################projectile asset
################################################### range ## cd #### target #### no of b.##### aoe ############# tower asset ######################################
    tower_types = {"test_tower_1"                 : (300, 1, 60  , 1, True, False, None,   1,  True,   100, 'tower_placeholder.png'            , 'bullet_placeholder.png'),
                   "test_tower_2"                 : (180, 2, 60  , 1, True,  True,    2,   1, False,  None, 'tower_placeholder.png'            , 'bullet_placeholder.png'),
                   "Algebra_basic"                : (500, 2, 30  , 1, True, False, None,  10, False,  None, 'Algebra_basic.png'                , 'Algebra_projectile.png'),
                   "Algebra_LT"                   : (500, 2, 30  , 1, True,  True,    4,  50, False,  None, 'Algebra_LT.png'                   , 'Algebra_projectile.png'),
                   "Algebra_complex_"             : (700, 4, 30  , 1, True, False, None,  50, False,  None, 'Algebra_complex_.png'             , 'Algebra_projectile.png'),
                   "Analysis_basic"               : (300, 2, 20  , 1, True, False, None,  10, False,  None, 'Analysis_basic.png'               , 'Analysis_projectile.png'),
                   "Analysis_calculus_specialist" : (300, 6, 20  , 1, True, False, None,  50,  True,   100, 'Analysis_calculus_specialist.png' , 'Analysis_projectile.png'),
                   "Analytic_functions_specialist": (300, 2,  8  , 1, True, False, None,  50, False,  None, 'Analytic_functions_specialist.png', 'Analysis_projectile.png'),
                   "Programming_basic"            : (300, 2, 20  , 1, True, False, None,  10,  True,   100, 'Programming_basic.png'            , 'Programming_projectile.png'),
                   "Programming_object"           : (300, 4, 30  , 1, True, False, None,  50,  True,   200, 'Programming_object.png'           , 'Programming_projectile.png'),
                   "Programing_spaghetti_decoder" : (300, 1, 60  , 1, True,  True,   10, 100, False,  None, 'Programing_spaghetti_decoder.png' , 'Spaghetti_projectile.png')
                   }
    """
        Tower stats positions:
        0 - range
        1 - damage
        2 - cooldown - later attributed to .atk
        3 - number of shots - not implemented
        4 - targeting - not implemented
        5 - bouncing
        6 - number of bounces
        7 - tower cost
        8 - aoe?
        9 - aoe range
        10 - tower asset
        11 - projectile asset
    """
    tower_upgrades = (("Algebra_basic", "Algebra_LT", "Algebra_complex_"),
                      ("Analysis_basic", "Analysis_calculus_specialist", "Analytic_functions_specialist"),
                      ("Programming_basic", "Programming_object", "Programing_spaghetti_decoder"))
    def __init__(self, tower_type: str = "test_tower") -> None:
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

    def setbasecooldown(self):
        """Resets the attack cooldown to the base cooldown value."""
        self.atk = self.base_cooldown

class Projectiles:
    """
    Manages projectiles fired by towers
    Takes start : Coord and finish : Coord arguments relating to position of
    their spawn and position where they should despawn.
    Asset : str argument defines graphic to be displayed
    Speed : int argument defines number of pixels travelled per frame
    Class attributes:
    displayed: list['Projectiles'] follows all existing projectiles
    """
    displayed: list['Projectiles']= []
    def __init__(self,start: Coord, finish: Coord, asset: str, speed: int = 60):
        self.asset = asset
        self.start = start
        # Self.start is constant, self.pos will be changed
        self.pos: Coord = start
        self.destination = finish
        self.speed = speed
        # Position on screen
        self.display_pos = ((self.pos - 25).x, (self.pos - 25).y)
        # Travelled distance
        self.travelled = 0
        # For clarity in init, these will be defined in separate method
        self.mov_vector = None
        self.vector_len = None
        Projectiles.displayed.append(self)
    def display_update(self):
        """Makes sure screen position stays bounded to actual position"""
        self.display_pos = ((self.pos - 25).x, (self.pos - 25).y)
    def create_vector(self):
        """Defines mov_vector and vector_len attributes"""
        base_vector = self.destination - self.start
        self.vector_len = (base_vector.x**2 + base_vector.y**2)**0.5
        # Vector of length 1
        normalized_vector = Coord(base_vector.x/self.vector_len,base_vector.y/self.vector_len)
        # Vector of length equal to speed
        self.mov_vector = Coord(normalized_vector.x*self.speed,normalized_vector.y*self.speed)
    def animation (self):
        """
        Takes care of proper initialization, removing and movement of projectiles
        """
        if not self.mov_vector:
            self.create_vector()
        if self.travelled > self.vector_len:
            self.remove()
        else:
            # Move projectile
            self.pos += self.mov_vector
            self.pos.ceiling()
            # Update travelled distance
            self.travelled += self.speed
            # Update position on screen
            self.display_update()
    def remove(self):
        """Deletes projectile"""
        Projectiles.displayed.remove(self)
    @classmethod
    def update(cls):
        """Animates all projectiles"""
        for projectile in cls.displayed:
            projectile.animation()
        if not EnemyManager.present:
            cls.displayed = []

class Tower_Manager:
    """
    Manages tower instances, handling their placement, attacks, and interactions with enemies.

    Class Attributes:
    towers (list['Tower_Manager']): Attribute storing all currently placed towers.
    enemies (list['Enemy']): Attribute referencing the list of active enemies from the EnemyManager class.
    explosions (list[list[tuple, int, int]]) : List of ongoing explosions.
    
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
    get_tower_positions(cls) -> dict[Coord, str]:
        Returns all towers currently on the map as dict keyed by their positions and valued with corresponding tower names.
    """

    towers: list['Tower_Manager'] = []
    enemies: list['EnemyManager'] = EnemyManager.present
    # list[list[tuple: explosion display position, int - aoe_range, int - remaining frames of displaying - 10 at the start]] - not implemented
    explosions: list[list[tuple, int, int]] = [] 

    def __init__(self,
                 tower_type_str: str = "test_tower", 
                 pos: Coord = Coord(0, 0)) -> None:
        """
        Initializes a tower at the specified position with the specified type.

        Arguments:
        tower_type_str (str):
            The type of tower to be created (default is "test_tower").
        pos (Coord):
            The position to place the tower on the map.
        """
        self.tower_type = Tower(tower_type_str)
        self.pos = Coord((pos.x//120)*120,(pos.y//120)*120) + 60
        self.display_pos = (self.pos.x - 60,self.pos.y-60)
        self.own_projectiles: list[Projectiles] = []
        # Criteria for choosing attack target. Currently only attacks the weakest.
        self.target_criteria = 'low_hp'
        # As bouncing attacks take multiple frames, they need more attributes
        if self.tower_type.bouncing:
            self.remaining_bounces = self.tower_type.bouncing_count
            # List following enemies and nearby targets for next bounce
            self.distance: list[(int,EnemyManager)] = []
            self.already_attacked: list[EnemyManager] = []
            self.next_target: EnemyManager = None
        Tower_Manager.towers.append(self)

    def untargetted_attack(self):
        """Manages untargetted attacks"""

    def attack(self):
        """Manages attacks, targeting the weakest enemy within range if the tower is ready to fire."""
        criteria = self.target_criteria
        for projectile in self.own_projectiles:
            if projectile not in Projectiles.displayed: #Removing unnecessary reference
                self.own_projectiles.remove(projectile)
        #Passing time between attacks
        if self.tower_type.atk !=0:
            self.tower_type.cooldown()
            # Processes bouncing attacks - they take more then one frame to be completed
            if self.tower_type.bouncing:
                if self.remaining_bounces and (self.distance or self.already_attacked):
                    for possible_target in self.distance:
                        # Finds non-attacked enemies within bounce range
                        if possible_target[0] <= 300 and possible_target[1] not in self.already_attacked:
                            previous: EnemyManager = self.next_target
                            # Mark enemy as attacked
                            self.already_attacked.append(possible_target[1])
                            self.next_target: EnemyManager  = possible_target[1]
                            self.next_target.take_damage(self.tower_type.dmg)
                            self.remaining_bounces -= 1
                            # Create projectile
                            self.own_projectiles.append(Projectiles(previous.pos,self.next_target.pos,self.tower_type.projectile_asset))
                            # Clear list of nearby enemies
                            self.distance = []
                            # Create new one
                            for victim in self.enemies:
                                area = ((victim.pos.x - self.next_target.pos.x)**2 + (victim.pos.y - self.next_target.pos.y)**2)**0.5
                                self.distance.append((area, victim))
                            self.distance.sort(key = lambda victim: victim[0])
                            break
                else:
                    self.distance.clear()
                    self.already_attacked.clear()
        #if tower is ready to fire, it will look for enemies in range
        else:
            if self.tower_type.bouncing:
                # Restore base bounces
                self.remaining_bounces = self.tower_type.bouncing_count
            inrange: dict[EnemyManager, Enemy.life]= {}#this dict will contain enemies in range as keys and their hp as values
            for enemy in Tower_Manager.enemies:
                distance = ((enemy.pos.x - self.pos.x)**2 + (enemy.pos.y - self.pos.y)**2)**0.5#calculates distance between tower and enemy
                if distance <= self.tower_type.range: #lists enemies within range (idea: we could use non-carthesian spaces)$$ #############coord class required###########
                    inrange[enemy] = (enemy.life)
            if not len(inrange):# returns when list length is 0
                return
            # Find enemies matching criteria - currently only lowest hp
            for enemy in inrange.keys():
                if criteria == 'low_hp':
                    value = inrange[enemy]
                    condition = min(inrange.values())
                # Not implemented
                #elif criteria == 'high_hp':
                #    value = inrange[enemy]
                #    condition = max(inrange.values())
                #elif criteria == 'front':
                #    value = inrange[enemy][1]
                #    condition = max(inrange.values()[1])
                #elif criteria == 'back':
                #    value = inrange[enemy][1]
                #    condition = min(inrange.values()[1])
                if value == condition:
                    target = enemy
                    # Determine attack type
                    if self.tower_type.aoe: 
                        for victims in self.enemies:
                            # Determine distance between first and surrounding targets
                            area = ((victims.pos.x - target.pos.x)**2 + (victims.pos.y - target.pos.y)**2)**0.5
                            if area <= self.tower_type.aoe_range:
                                victims.take_damage(self.tower_type.dmg)
                        # Create projectiles
                        self.own_projectiles.append(Projectiles(self.pos, enemy.pos, self.tower_type.projectile_asset))
                        # Explosion animation - not implemented
                        Tower_Manager.explosions.append([(enemy.pos.x - self.tower_type.aoe_range,enemy.pos.y - self.tower_type.aoe_range),self.tower_type.aoe_range,10])
                        # Restore cooldown
                        self.tower_type.setbasecooldown()
                        break
                    elif self.tower_type.bouncing:
                        self.next_target = target
                        enemy.take_damage(self.tower_type.dmg)
                        self.own_projectiles.append(Projectiles(self.pos,self.next_target.pos,self.tower_type.projectile_asset))
                        self.already_attacked = [self.next_target]
                        #for bounce in range(self.tower_type.bouncing_count):
                        self.distance = []
                        # Explained in first if in Attack()
                        for victim in self.enemies:
                            area = ((victim.pos.x - self.next_target.pos.x)**2 + (victim.pos.y - self.next_target.pos.y)**2)**0.5
                            self.distance.append((area, victim))
                        self.distance.sort(key = lambda victim: victim[0])
                        self.tower_type.setbasecooldown()
                        break
                    else:
                        enemy.take_damage(self.tower_type.dmg)
                        self.tower_type.setbasecooldown()
                        self.own_projectiles.append(Projectiles(self.pos,enemy.pos,self.tower_type.projectile_asset))
                        break

    def upgrade(self, tower_name : str):
        """This method upgrades a chosen tower by deleting old an placing new""" 
        pos = self.pos
        new_tower = Tower_Manager(tower_name,pos)
        Tower_Manager.towers.remove(self)
        

    @classmethod
    def explosions_update(cls):
        for explosion in cls.explosions:
            if explosion[2] == 0:
                cls.explosions.remove(explosion)
        for explosion in cls.explosions:
            explosion[2] -= 1

    @classmethod
    def update(cls):
        """Update all active towers, managing their attacks every frame."""
        cls.enemies = EnemyManager.present #update enemy list
        for tower in cls.towers:
            tower.attack()
        Projectiles.update()
        cls.explosions_update()

    @classmethod
    def reset(cls):
        """Clearsall towers, when new game starts"""
        cls.towers = [] # clearing list
        
    def load_lvl():
        """Clear old data and reset towers, used when loading a new level."""
        Tower_Manager.reset()

    @classmethod
    def get_tower_positions(cls) -> dict[Coord, str]:
        """
        Returns all towers on the map 
        as the dictionary keyed by tile coordinates on which there are towers
        and valued by the corresponding tower names
        """
        return {Coord.res2tile(tuple(tower.pos)) : tower.tower_type.tower_name for tower in cls.towers}
        