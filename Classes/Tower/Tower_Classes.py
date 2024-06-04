"""Tower meneger module"""

from ..Utilities import Coord
from ..Level import Test_Level

class Tower: #defining properties of towers
    def __init__(self, tower_type : str = "test_tower",
                 tower_types : dict[str : tuple[int, int, int, int, bool, bool]] = None) -> None:
        """
        Initializes tower of type tower_type

        tower_types content:
            - range in pixels
            - demage
            - atk_speed will in fact be delay between other attacks
            - number of projectiles fired
            - some towers will fire projectiles in predefined directions (at some point)
            - some towers will fire projectiles in predefined directions (at some point)
        """
        # Set tower_types dict if not given
        if tower_types is None:
            tower_types = {"test_tower" : (10, 10, 10, 10, False, False)}

        # Initialize tower
        self.range, \
        self.dmg, \
        self.atk, \
        self.shot_count, \
        self.targeting, \
        self.bouncing \
            = tower_types[tower_type]

class Tower_Manager:
    """This class is responsible for storing information about towers and attacking enemies"""
    towers = []

    def __init__(self,
                 level : Test_Level.Level,
                 tower_type : str = "test_tower", 
                 pos : Coord = Coord(0, 0), 
                 enemies : list = None) -> None:
        "Place tower"
        Tower_Manager.towers.append(Tower(tower_type))
        level.map.grid[pos] = True


    """
    def __init__(self,tower_type : Tower,coord,enemies):############requires integration with coord class
        self.tower_type = tower_type
        self.coord = coord ############## coord
        self.grid_loc = [((coord[0]//16)*120)+60,((coord[1]//9)*120)+60] ###### placement on the grid ######### currently unutilised for simplicity in test text game ##############!!############ coord class required
        self.enemies = enemies #assuming all enemies coords can be accesed through list ## not needed when enemies will be accessible through level entity attribute ###############!!
        Tower_Manager.towers.append((tower_type,coord)) #list of all placed towers
    """
    @classmethod
    def reset(cls):
        cls.towers = [] #clearing list

    def attack(self):
        inrange = []
        for enemy in self.enemies:
            if ((enemy[1][0]-self.coord[0])**2 + (enemy[1][1]-self.coord[1])**2)**0.5 <= self.tower_type.range: #lists enemies within range (idea: we could use non-carthesian spaces)$$ #############coord class required###########
                inrange.append(enemy)
        for enemy in inrange:
            if enemy[0] == min([enemyhp[0] for enemyhp in inrange]): #defaults to attacking weakest enemies, might be choose-able later.$$
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
                if enemy[0] <= self.tower_type.dmg: #checks if attack will kill enemy
                    self.enemies.remove(enemy)
                    #flag = 'enemy_died' #for debug
                    break #at the moment first closest enemy on the list will be attacked
                else:
                    enemy[0] -= self.tower_type.dmg #attack itself
                    #flag = 'enemy_attacked' #for debug
                    break

