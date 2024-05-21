"""Map generator"""


# IMPORTS
import pygame
import random
import sys
import os
import map_generator_classes as MAP


# CONSTANTS
CURRENT_DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__)) # get the current directory path
TILES_PATH = CURRENT_DIRECTORY_PATH + "\\tiles"
FPS = 60 # framerate
RESOLUTION = 1920, 1080

# SET UP WONDOW AND PYGAME
# initialize Pygame
pygame.init()
# set up the full-screen mode and resolution
screen = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
# set the title of the window
pygame.display.set_caption('STUDENTS DEFENSE - MAP GENERATOR')


# INITIALIZE UTILITY VARIABLES
# variable for menaging frame rate
clock = pygame.time.Clock()
pos = pygame.mouse.get_pos()
mouse_click = False
board = MAP.Map.random_map(TILES_PATH, screen)
print("Initialized board:\n")
print(board)

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

            elif event.key == pygame.K_SPACE:
                board = MAP.Map.random_map(TILES_PATH, screen)
                print("Initialized board:\n")
                print(board)

        # mouse press (relise)
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            mouse_click = True
                    


    
    # DRAW WINDOW CONTENTS
    # fill the screen with black background 
    screen.fill((0, 0, 0))
    # draw board
    board.draw()
    

    # UPDATE STUFF
    # window updates
    pygame.display.flip() # update the display
    clock.tick(FPS) # ensure up to 60 fps

# quit Pygame and program
pygame.quit()
sys.exit()
