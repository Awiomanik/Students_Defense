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
# obsticles
show_grid = False
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
path_button_pressed_txt = font_buttons.render("PATH BUILDER", True, (0, 255, 0))
obsticle_button_txt = font_buttons.render("SET OBSTICLES", True, (0, 0, 0))
obsticle_button_pressed_txt = font_buttons.render("SET OBSTICLES", True, (0, 255, 0))
grid_button_txt = font_buttons.render("SHOW GRID", True, (0, 0, 0))
grid_button_pressed_txt = font_buttons.render("SHOW GRID", True, (0, 255, 0))
path_instruction = font_instructions.render("PATH BUILDER: Place a path segment with a left mouse button, remove last path segment with right mouse button.", True, (0, 0, 0))

# HELPER FUNCTIONS
def draw_grid():
    # Set the color for the grid lines
    grid_color = (0, 0, 0)  # White
    col_len = RESOLUTION[1] - 240
    row_len = RESOLUTION[0] 

    # Draw vertical lines
    for col in range(16):
        x = col * 120
        pygame.draw.line(screen, grid_color, (x, 0), (x, col_len), 2)

    # Draw horizontal lines
    for row in range(7):
        y = row * 120
        pygame.draw.line(screen, grid_color, (0, y), (row_len, y), 2)


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
            print("mouse click at position:", pos)
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
    if state != "path":
        screen.blit(path_button_txt, (220, 895))
    if show_grid:
        screen.blit(grid_button_pressed_txt, (530, 895))
        draw_grid()
    else:
        screen.blit(grid_button_txt, (530, 895))
    if state != "obsticles":
        screen.blit(obsticle_button_txt, (1234, 895))
    else:
        screen.blit(obsticle_button_pressed_txt, (1234, 895))


    # ACTIONS
    # None
    if state == "idle":
        if mouse_click_left:
            x, y = pos
            if 860 < y < 980:
                mouse_click_left = False
                # path
                if 180 < x < 420:
                    state = "path"
                # grid
                elif 480 < x < 620:
                    show_grid = not show_grid
                # obsticles
                elif 1200 < x < 1320:
                    state = "obsticles"
                # save
                elif 1500 < x < 1620:
                    print(board.save())
    # path builder
    if state == "path":
        screen.blit(path_button_pressed_txt, (220, 895))
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
    # obsticle builder
    if state == "obsticles":
        if mouse_click_left:
            board.add_obsticle(pos)
        elif mouse_click_right:
            board.remove_obsticle(pos)

        if mouse_click_left and 860 < pos[1] < 980 and 1200 < pos[0] < 1320:
            state = "idle"


    # UPDATE STUFF
    # Window updates
    pygame.display.flip() # update the display
    clock.tick(FPS) # ensure up to 60 fps
    # Get mouse podition in pixels
    pos = pygame.mouse.get_pos()
    mouse_click_left = mouse_click_right = False
    
# quit Pygame and program
pygame.quit()
sys.exit()
