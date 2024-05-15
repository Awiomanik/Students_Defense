# prototipical enemy class

# IMPORTS
import pygame
import random

class Enemy:
    enemy_count = 0

    def __init__(self, 
                 graphic_path:str, 
                 path_to_follow:list[tuple[int,int]],
                 path_widths:list[int],
                 size:tuple[int,int]=(100, 100), 
                 speed:int=5,
                 health:int=100) -> None:

        # basic enemy parameters
        self.health = health
        self.size = size

        # positions and speeds
        self.pos = pygame.math.Vector2(path_to_follow[0])# initializing strating position
        self.circle_pos = pygame.math.Vector2(path_to_follow[0]) # initializing again for circle to not work on same list
        self.circle_target = pygame.math.Vector2(path_to_follow[1])
        self.current_circle_direction = pygame.math.Vector2((self.circle_target - self.circle_pos).normalize())
        self.path_index = 1
        self.path = path_to_follow
        self.path_widths = [path_widths[0]] + path_widths + [path_widths[-1]]
        self.speed = speed
        self.local_speed = pygame.math.Vector2(0, 0)
        self.current_circle_radius = path_widths[1]
        self.circle_pos2 = pygame.math.Vector2(0, 0)

        # load image and scale it to given size
        self.face = pygame.transform.scale(pygame.image.load(graphic_path), size)

        # update enemy counter
        Enemy.enemy_count += 1

    def move_circle(self) -> None:

        # if current position of circle at target position
        if self.circle_pos.distance_to(self.circle_target) <= self.speed:
            self.circle_pos = self.circle_target.copy()  # snap to the target if close enough

            # if current target not the endpoint
            if self.path_index < len(self.path) - 1:
                self.path_index += 1
                self.circle_target = pygame.math.Vector2(self.path[self.path_index])
                self.current_circle_direction = pygame.math.Vector2((self.circle_target - self.circle_pos).normalize())
            else:
                print("Enemy reached end point!")
        # move the circle
        else:   
            self.circle_pos += self.current_circle_direction * self.speed  # move towards the target

        # update circle size
        self.current_circle_radius = min(self.path_widths[self.path_index], 
                                         self.circle_pos.distance_to(self.circle_target) + self.path_widths[self.path_index+1], 
                                         self.circle_pos.distance_to(self.path[self.path_index-1]) + self.path_widths[self.path_index-1])

    def move_enemy(self) -> None:
        if self.current_circle_radius > self.size[0]:
            # update position within circle
            self.pos += self.local_speed + self.current_circle_direction * self.speed

            # check if enemy is outside the circle and adjust
            if (self.pos - self.circle_pos).length() > self.current_circle_radius - max(self.size)//2:
                direction = (self.pos - self.circle_pos).normalize()
                self.pos = self.circle_pos + direction * (self.current_circle_radius - max(self.size))

                # reverse the speed component along the wall of the circle
                self.local_speed = self.current_circle_direction * self.speed
                

            # updagte local speed
            temp = self.speed / 5
            self.local_speed.x += random.uniform(-temp, temp)
            self.local_speed.y += random.uniform(-temp, temp)
            if self.pos != self.circle_pos: self.local_speed -= (self.pos - self.circle_pos).normalize()

            self.circle_pos2 = (self.pos - self.circle_pos) * (self.current_circle_radius - max(self.size)) 

        else:
            randx, randy = random.randint(-1, 1), random.randint(-1, 1)
            if abs(self.circle_pos2.x + randx) > self.current_circle_radius: randx = - randx
            if abs(self.circle_pos2.y + randy) > self.current_circle_radius: randy = - randy
            self.circle_pos2 += pygame.math.Vector2(randx, randy)
            self.pos = self.circle_pos + self.circle_pos2

    def update(self) -> None:
        self.move_circle()
        self.move_enemy()

    def draw(self, screen, test=False):
        if test: pygame.draw.circle(screen, (0, 255, 0), (int(self.circle_pos.x), int(self.circle_pos.y)), self.current_circle_radius, 1)
        screen.blit(self.face, (int(self.pos.x) - self.size[0] // 2, int(self.pos.y) - self.size[1] // 2))


