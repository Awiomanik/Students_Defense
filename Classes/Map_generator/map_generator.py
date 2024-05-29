"""Map generator"""


# IMPORTS
import pygame
import sys
import os
from . import map_generator_classes as MAP


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
mouse_click_left = mouse_click_right = False
state = "idle"
# possible states:
# idle
# path 
# obsticle
pos = pygame.mouse.get_pos()
board = MAP.Map.grass_map(TILES_PATH, screen)
print("Initialized board:\n")
print(board)

# Get UI elements
title = pygame.image.load(CURRENT_DIRECTORY_PATH + "\\UI_assets\\TXT_MAP_CREATOR.png")
button = pygame.image.load(CURRENT_DIRECTORY_PATH + "\\UI_assets\\BLANK_BUTTON.png")
font_buttons = pygame.font.SysFont('Impact', 30)
font_instructions = pygame.font.SysFont('Consolas', 24)
path_button_txt = font_buttons.render("PATH BUILDER", True, (0, 0, 0))
path_instruction = font_instructions.render("PATH BUILDER: Place a path segment with a left mouse button, remove last path segment with right mouse button.", True, (0, 0, 0))


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

        # mouse press (relise)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_click_left = True
            if event.button == 3:
                mouse_click_right = True
                    
    
    # DRAW WINDOW CONTENTS
    # fill the screen with black background 
    screen.fill((0, 0, 0))
    # draw board
    board.draw()
    # draw accessibility rectangle
    if state == "path" and pos[1] < 840:
        board.tile_accessibility(pos)
    # Draw UI
    # Draw title
    screen.blit(title, (780, 860))
    # Draw buttons
    screen.blit(button, (180, 860))
    screen.blit(button, (480, 860))
    screen.blit(button, (1200, 860))
    screen.blit(button, (1500, 860))
    # Print text on buttons
    screen.blit(path_button_txt, (220, 895))



    # ACTIONS
    # None
    if state == "idle":
        if mouse_click_left:
            x, y = pos
            # path
            if 180 < x < 300 and 860 < 980:
                state = 'path'
            # obsticles
            # grid
            # save
    # path builder
    if state == "path":
        if board.valid:
            board.clear_paths()

        screen.blit(path_instruction, (30, 1030))
        # Set a tile
        if mouse_click_left:
            mouse_click_left = False
            if board.tile_accessibility(pos, False):
                if board.add_path(pos):
                    state = "idle"
                print(board)
        # Remove a tile
        if mouse_click_right:
            mouse_click_right = False
            board.remove_path()
            print(board)    

    # UPDATE STUFF
    # Window updates
    pygame.display.flip() # update the display
    clock.tick(FPS) # ensure up to 60 fps
    # Get mouse podition in pixels
    pos = pygame.mouse.get_pos()
    
# quit Pygame and program
pygame.quit()
sys.exit()
