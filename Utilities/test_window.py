"""Testing pygame functionlities."""


# IMPORTS
import pygame
import random
import sys
import os

import pygame.gfxdraw
from test_level.test_enemy import Enemy
from test_level.test_map import Map as Board
from test_level.UI import UI
from test_level.test_tower import Defense


# CONSTANTS
CURRENT_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__)) # get the current directory path
MAP_IMAGE_PATH = CURRENT_DIRECTORY_PATH + "\\test_level\\graphics\\maps\\Kampus_Pwr_edit.png"
#MAP_IMAGE_PATH = CURRENT_DIRECTORY_PATH + "\\test_level\\graphics\\maps\\Kampus_Pwr.png"
#MAP_IMAGE_PATH = CURRENT_DIRECTORY_PATH + "\\test_level\\graphics\\maps\\test_background_gpt.jpg.png"
#MAP_IMAGE_PATH = CURRENT_DIRECTORY_PATH + "\\test_level\\graphics\\maps\\test_background_simple.png"
ENEMY_IMAGE_PATH = CURRENT_DIRECTORY_PATH + "\\test_level\\graphics\\enemies\\chicken.png"
TOWERS_PATH = CURRENT_DIRECTORY_PATH + "\\test_level\\graphics\\towers"
FPS = 60 # framerate
RESOLUTION = 1920, 1080
#enemy_size = 40
#enemy_speed = 5
enemy_size = 30
enemy_speed = 5
enemy_local_speed = 5

# SET UP WONDOW AND PYGAME
# initialize Pygame
pygame.init()
# set up the full-screen mode and resolution
screen = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
# set the title of the window
pygame.display.set_caption('STUDENTS DEFENSE')


# INITIALIZE SUPPORTING CLASSES
board = Board(MAP_IMAGE_PATH, TOWERS_PATH, RESOLUTION)
ui = UI([board.towers[0][0]], [(1700, 850)])
defense = Defense(TOWERS_PATH + "\\sky_tower.png", (10, 10))


# INITIALIZE UTILITY VARIABLES
# variable for menaging frame rate
clock = pygame.time.Clock()
enemies = []
mouse_pos = None
placing_tower = False
towers = []
wrong_place = False
wrong_place_size = 20

# MAIN LOOP
running = True
while running:

    # HANDLE EVENTS (eg. key press)
    for event in pygame.event.get():
        # quit game if is being window closed
        if event.type == pygame.QUIT:
            running = False
        # key press
        elif event.type == pygame.KEYDOWN:
            # temporary exit way (escape key)
            if event.key == pygame.K_ESCAPE:
                running = False
            # drop chicken
            if event.key == pygame.K_SPACE:
                enemies.append(Enemy(ENEMY_IMAGE_PATH, 
                                     board.enemies_path, 
                                     board.enemies_path_widths, 
                                     enemy_size, enemy_speed, 
                                     random.randint(0, enemy_local_speed)))
        # mouse press (relise)
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            #print(pos)

            if pos[0] > 1700 and pos[1] > 850: 
                placing_tower = not placing_tower

            elif placing_tower:
                if defense.occupied(((temp:=pygame.math.Vector2(pos)), temp + pygame.math.Vector2(225, 150))):
                    wrong_place = True
                else:
                    towers.append(Defense(TOWERS_PATH + "\\sky_tower.png", (pos[0] - 100, pos[1] - 100)))
                    placing_tower = not placing_tower
                    


    
    # DRAW WINDOW CONTENTS
    # fill the screen with black background 
    #screen.fill((0, 0, 0))
    # background
    board.draw(screen)
    # enemies
    for enemy in enemies: 
        enemy.draw(screen)#, True)
    # towers (UI)
    ui.draw(screen)
    # tower placement
    if placing_tower:
        x, y = pygame.mouse.get_pos()
        screen.blit(defense.face, (x - 100, y - 100))
    # towers
    for tower in towers:
        tower.draw(screen)
    # wrong place
    if wrong_place: 
        if wrong_place_size < 200:
            pygame.gfxdraw.filled_circle(screen, pos[0], pos[1], wrong_place_size, (255, 0, 0, 80))
            wrong_place_size += 60
        else:
            wrong_place_size = 20
            wrong_place = False

    

    # UPDATE STUFF
    # window updates
    pygame.display.flip() # update the display
    clock.tick(FPS) # ensure up to 60 fps
    # move chickens
    for enemy in enemies[:]: # shallow copy of list enables to remove from list in for loop
        # if enemy reached the endpoint, remove it from the list
        if enemy.update():
            enemies.remove(enemy)

# quit Pygame and program
pygame.quit()
sys.exit()
