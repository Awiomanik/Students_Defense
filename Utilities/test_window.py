"""Testing pygame functionlities."""


# IMPORTS
import pygame
import random
import sys
import os
from test_level.test_enemy import Enemy
from test_level.test_map import Map as Board


# CONSTANTS
CURRENT_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__)) # get the current directory path
MAP_IMAGE_PATH = CURRENT_DIRECTORY_PATH + "\\test_level\\graphics\\maps\\Kampus_Pwr_edit.png"
#MAP_IMAGE_PATH = CURRENT_DIRECTORY_PATH + "\\test_level\\graphics\\maps\\Kampus_Pwr.png"
#MAP_IMAGE_PATH = CURRENT_DIRECTORY_PATH + "\\test_level\\graphics\\maps\\test_background_gpt.jpg.png"
#MAP_IMAGE_PATH = CURRENT_DIRECTORY_PATH + "\\test_level\\graphics\\maps\\test_background_simple.png"
ENEMY_IMAGE_PATH = CURRENT_DIRECTORY_PATH + "\\test_level\\graphics\\enemies\\chicken.png"
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
board = Board(MAP_IMAGE_PATH, RESOLUTION)


# INITIALIZE UTILITY VARIABLES
# variable for menaging frame rate
clock = pygame.time.Clock()
enemies = []

# MAIN LOOP
running = True
while running:

    # HANDLE EVENTS (eg. key press)
    for event in pygame.event.get():
        # quit game if is being window closed
        if event.type == pygame.QUIT:
            running = False
        # temporary exit way (escape key)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # drop chicken
            if event.key == pygame.K_SPACE:
                enemies.append(Enemy(ENEMY_IMAGE_PATH, 
                                     board.enemies_path, 
                                     board.enemies_path_widths, 
                                     enemy_size, enemy_speed, 
                                     random.randint(0, enemy_local_speed)))

    
    # DRAW WINDOW CONTENTS
    # fill the screen with black background 
    #screen.fill((0, 0, 0))
    # background
    map.draw(screen)
    # enemies
    for enemy in enemies: 
        enemy.draw(screen, True)
    

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
