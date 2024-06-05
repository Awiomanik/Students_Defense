
#they should have they life, speed, image and position
#they can move and take damage 
#at the moment enemy can only move forward

class Enemy():
    def __init__(self, life: int, speed: int, position):
        self.life = life
        self.speed = speed
        self.rect.center = position

    def move(self):
        self.rect.x += 1

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
    
#class Enemy_Manager:
#    present = []
#    def __init__(self,enemy : Enemy):
#        Enemy_Manager.present.append(enemy)
#    @classmethod
#    def remove_enemy(cls):
#        for enemy in Enemy_Manager.present:
#            if enemy.life == 0

