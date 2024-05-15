# Testing pygame functionlities


# IMPORTS
import pygame
import sys
import os
from test_level.test_enemy import Enemy
from test_level.test_map import Map


# CONSTANTS
CURRENT_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__)) # get the current directory path
GRAPHICS_PATH = CURRENT_DIRECTORY_PATH + "\\test_level\\graphics\\" # path to graphic files
FPS = 60 # framerate
RESOLUTION = 1920, 1080


# IMAGES
background_image = GRAPHICS_PATH + 'Kampus_Pwr_edit.png'
#background_image = GRAPHICS_PATH + 'Kampus_Pwr.png'
#background_image = GRAPHICS_PATH + 'test_background_gpt.jpg'
#background_image = GRAPHICS_PATH + 'test_background_simple.png'

enemy_image = GRAPHICS_PATH + "chicken.png"
#enemy_size = (40, 40)
#enemy_speed = 5
enemy_size = (30, 30)
enemy_speed = 2

# SET UP WONDOW AND PYGAME
# initialize Pygame
pygame.init()
# set up the full-screen mode and resolution
screen = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
# set the title of the window
pygame.display.set_caption('STUDENTS DEFENSE')


# INITIALIZE SUPPORTING CLASSES
map = Map(background_image, RESOLUTION)


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
                enemies.append(Enemy(enemy_image, map.enemies_path, map.enemies_path_widths, enemy_size, enemy_speed))

    
    # DRAW WINDOW CONTENTS
    # fill the screen with black background 
    #screen.fill((0, 0, 0))
    # background
    map.draw(screen)
    # enemies
    for enemy in enemies: enemy.draw(screen)#, True)
    

    # UPDATE STUFF
    # window updates
    pygame.display.flip() # update the display
    clock.tick(FPS) # ensure up to 60 fps
    # move chickens
    for enemy in enemies: enemy.update()

# quit Pygame and program
pygame.quit()
sys.exit()
