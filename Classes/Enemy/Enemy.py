from ..Utilities import Coord
#they should have they life, speed, image and position
#they can move and take damage 
#at the moment enemy can only move forward

class Enemy:
    test = []
    def __init__(self, life: int, speed: int, position : Coord):
        self.life = life
        self.speed = speed
        self.pos = position

    def move_x_up(self):
        self.pos.x += self.speed

    def move_x_down(self):
        self.pos.x -= self.speed
    
    def move_y_right(self):
        self.pos.y += self.speed
    def move_y_left(self):
        self.pos.y -= self.speed
    def update(self):
        self.move()

    def take_damage(self, damage):
        self.life -= damage
        if self.life < 0:
            self.life = 0

    def is_alive(self):
        return self.life > 0
    
    def __str__(self):
        return f"Enemy(life={self.life}, speed={self.speed})"
    
class Enemy_Manager:
    present = []
    def __init__(self,enemy : Enemy):
        Enemy_Manager.present.append(enemy)
    @classmethod
    def remove_enemy(cls):
        for enemy in Enemy_Manager.present:
            if enemy.life == 0:
                cls.present.remove(enemy)
    def endlevel(cls):
        cls.present = []