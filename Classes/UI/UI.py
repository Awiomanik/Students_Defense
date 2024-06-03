"""This module contains UI class for drawing game on the screen (and possibly audio)"""

# IMPORTS
import pygame, os, sys

class UI():
    """
    """
    FPS : int = 60 # framerate
    RESOLUTION : tuple[int, int] = 1920, 1080

    def __init__(self) -> None:
        # SET UP WONDOW AND PYGAME
        # initialize Pygame
        pygame.init()
        # set up the full-screen mode and resolution
        self.screen = pygame.display.set_mode(self.RESOLUTION, pygame.FULLSCREEN)
        # set the title of the window
        pygame.display.set_caption("STUDENTS DEFENSE")

        # INITIALIZE UTILITY VARIABLES
        # variable for menaging frame rate
        self.clock = pygame.time.Clock() 
        # varibles for menaging user mouse input
        self.mouse_click = False 
        self.pos = pygame.mouse.get_pos()

        # SET ASSETS PATHS
        self.gfx_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Assets", "gfx")
        # audio path (in the future)
        
    def intro(self) -> None:
        # Write down title character by character on the center of the screen
        font = pygame.font.SysFont('Consolas', 200)
        title = "Hello World!"
        # Iterate ovr charachters
        for i in range(len(title)):
            # Do not devote time for spaces
            if (title[i] == ' '):
                continue
            # Fill screen with black
            self.screen.fill((0, 0, 0))
            # Render text up to i'th character
            text = font.render(title[:i + 1], True, (0, 255, 0))
            # Center the rectangle on the screen
            text_rect = text.get_rect()
            text_rect.center = (self.RESOLUTION[0] // 2, self.RESOLUTION[1] // 2)
            # Blit the text
            self.screen.blit(text, text_rect)
            # Update pygame and clock every 0.5s
            pygame.display.update()
            self.clock.tick(self.FPS//30)

        # Wait for a secound after writing finnished
        pygame.time.delay(1000)

    def main_menu(self) -> bool:
        main_menu_graphic = pygame.image.load(os.path.join(self.gfx_path, "main_menu.png"))
        self.screen.blit(main_menu_graphic, (0, 0))

        # Main menu loop
        running = True
        while running:

            # HANDLE EVENTS (eg. key press)
            for event in pygame.event.get():
                
                # quit game if is being window closed
                if event.type == pygame.QUIT:
                    running = False

                # mouse press (relise)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_click = True
                    self.pos = pygame.mouse.get_pos()

            # PROCESS INTERACTION
            if self.mouse_click:
                x, y = self.pos
                if 700 < x < 1300:
                    # start button pressed
                    if 325 < y < 600:
                        return True
                    # quit button pressed
                    elif 640 < y < 880:
                        pygame.quit()
                        sys.exit()

            # Update pygame and clock every 60'th of a secound
            pygame.display.flip()
            self.clock.tick(self.FPS)
        
    def load_lvl(self, 
                 map_name : str = "TEST_1", 
                 towers_names : dict = {"test_tower" : "tower_placeholder.png"},
                 bullets_names : dict = {"test_bullet" : "bullet_placeholder.png"}) -> None:
        # Load graphics
        self.map_gfx = pygame.image.load(os.path.join(self.gfx_path, "maps", map_name + "_map.png"))
        self.towers_gfx = {name : pygame.image.load(os.path.join(self.gfx_path, "towers", file)) 
                           for name, file in towers_names.items()}
        self.bullets_gfx = {name : pygame.image.load(os.path.join(self.gfx_path, "bullets", file))
                            for name, file in bullets_names.items()}        

    def update(self) -> None:
        # DRAW ELEMENTS
        self.screen.blit(self.map_gfx, (0, 0))

        # UPDATE SCREEN
        pygame.display.flip()
        self.clock.tick(self.FPS)


