from ..Utilities import Coord
from ..Map.Map_Class import Map

class Enemy:
    enemy_types = {'test_enemy':{'hp': 5, 'speed' : 3}}
    def __init__(self, enemy_type : str = 'test_enemy'):
        self.life = Enemy.enemy_types[enemy_type]['hp']
        self.speed = Enemy.enemy_types[enemy_type]['speed']
    
    def __str__(self):
        return f"Enemy(life={self.life}, speed={self.speed})"
    
class Enemy_Manager:
    present = []
    def __init__(self,enemy_type : str = 'test_enemy', map : Map = Map()):
        self.name = enemy_type
        self.map : Map = map
        self.path = map.paths[0]
        self.enemy_type = Enemy(enemy_type)
        self.speed = self.enemy_type.speed
        self.life = self.enemy_type.life
        self.pos : Coord = Coord(-80,self.path[0].y*120 + 60) #starts to the left of first path tile
        self.display_pos : tuple = (self.pos.x - 30,self.pos.y - 30)
        self.grid_pos = Coord(self.pos.x//120,self.pos.y//120)
        self.tile = 0
        self.hp_display = None #used in UI
        self.attacked = False
        self.attacked_count = None
        self.damaged_player = False
        Enemy_Manager.present.append(self)
    def __repr__(self) -> str:
        return(f"{self.name} enemy with {self.life} hp and {self.pos} position")
    def take_damage(self, damage):
        self.life -= damage
        if self.life < 0:
            self.life = 0
        self.attacked = True
        self.attacked_count = 5
    def remove_attacked(self):
        if self.attacked_count:
            self.attacked_count -=1
        else:
            self.attacked = False

    def movement(self):
        if self.tile < len(self.path):
            destination : Coord = self.path[self.tile] 
            direction : Coord = destination - self.grid_pos
            self.pos += Coord(self.speed*direction.x,self.speed*direction.y)
            self.grid_pos = Coord(self.pos.x//120,self.pos.y//120)
            self.display_pos : tuple = (self.pos.x - 30,self.pos.y - 30)
            if (self.grid_pos.x,self.grid_pos.y) == (destination.x,destination.y):
                self.tile += 1
        else: #once enemy enters last tile on path, it will only move to right until removed by remove_enemy
            self.pos += Coord(self.speed,0)
            self.display_pos : tuple = (self.pos.x - 30,self.pos.y - 30)
            if self.pos.x >= 1980 and not self.damaged_player:
                self.damaged_player = True
            if self.damaged_player == "done":
                Enemy_Manager.present.remove(self)

                
    def remove_enemy(self):
        if self.life == 0:
            Enemy_Manager.present.remove(self)
    @classmethod
    def endlevel(cls):
        cls.present = []
    @classmethod
    def update(cls):
        for enemy in cls.present:
            enemy.remove_enemy()
            enemy.movement()
            enemy.remove_attacked()
## TEST ##
#x = 0
#test = Enemy_Manager()
#while len(Enemy_Manager.present):
#    x+=1
#   print('pixel position:',test.pos,'grid position:',test.grid_pos)
#    Enemy_Manager.update()
#    if x == 20000:
#        break