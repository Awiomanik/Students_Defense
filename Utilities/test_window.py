# Testing pygame functionlities

# IMPORTS
import pygame
import sys
import random

# CONSTANTS
current_path = sys.path[0]
#print(current_path)
graphics_path = current_path + "\\test_level\\graphics\\"

# initialize Pygame
pygame.init()

# set up the full-screen mode
dis_info = pygame.display.Info()
screen = pygame.display.set_mode((dis_info.current_w, dis_info.current_h), pygame.FULLSCREEN)
enemies_pos = []
enemies_speeds = []
enemy_count = 0


# set the title of the window
pygame.display.set_caption('STUDENTS DEFENSE')

# variable for menaging frame rate
clock = pygame.time.Clock()

# Load images
background_image = pygame.image.load(graphics_path + 'test_background.jpg') # load image
background_image = pygame.transform.scale(background_image, (dis_info.current_w, dis_info.current_h))  # scale image to screen size
enemy_graphic = pygame.image.load(graphics_path + 'chicken.png')
enemy_graphic = pygame.transform.scale(enemy_graphic, (100, 100))


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
                enemies_pos.append([random.randint(100,  dis_info.current_w - 200), random.randint(100, dis_info.current_h - 200)])
                enemies_speeds.append([0, 0])
                enemy_count += 1
                print(enemy_count)

    
    # DRAW STUFF
    # fill the screen with black background 
    #screen.fill((0, 0, 0))
    # background
    screen.blit(background_image, (0, 0))
    # enemy
    for i in range(enemy_count):
        screen.blit(enemy_graphic, enemies_pos[i])
    

    # UPDATE STUFF
    # update the display
    pygame.display.flip()

    # ensure 60 fps
    clock.tick(60)


    # move chickens
    for i, (pos, speed) in enumerate(zip(enemies_pos, enemies_speeds)):

        enemies_speeds[i] = [speed[0] + random.randint(-1, 1), speed[1] + random.randint(-1, 1)]
        enemies_pos[i] = [pos[0] + speed[0], pos[1] + speed[1]]

        if enemies_pos[i][0] < 0:
            enemies_pos[i][0] = 0
            enemies_speeds[i][0] = 5
        if enemies_pos[i][1] < 0:
            enemies_pos[i][1] = 0
            enemies_speeds[i][1] = 5
        if enemies_pos[i][0] > dis_info.current_w-100:
            enemies_pos[i][0] = dis_info.current_w-100
            enemies_speeds[i][0] = -5
        if enemies_pos[i][1] > dis_info.current_h-100:
            enemies_pos[i][1] = dis_info.current_h-100
            enemies_speeds[i][1] = -5

        #print("Pos: ",dis_info.current_w, dis_info.current_h, enemy_pos)

# quit Pygame and program
pygame.quit()
sys.exit()
