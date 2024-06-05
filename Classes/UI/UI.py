"""
This module contains UI class for menaging interactions with user 
(inout from keyboard and mouse and drawing graphics (potentialy also sounds))
"""

# IMPORTS
import pygame, os, sys
from ..Game import Game
from ..Tower.Tower_Classes import Tower_Manager, Tower
from ..Utilities import Coord
from ..Player.Player import Player
from ..Map.Map_Class import Map as mp

class UI():
    """
    """
    state = "idle"
    FPS : int = 60 # framerate
    RESOLUTION : tuple[int, int] = 1920, 1080

    def __init__(self, player_name : str) -> None:
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

        # SET AND LOAD HUD ELEMENTS
        self.font = pygame.font.SysFont("Consolas", 50)
        player_name = player_name if len(player_name) < 20 else player_name[:17] + "..."
        self.player_name_gfx = self.font.render("Player:  " + player_name, False, (0, 0, 0))
        self.button_gfx = pygame.image.load(os.path.join(self.gfx_path, "HUD", "BLANK_BUTTON.png"))

    def get_input(self, map : mp, player : Player) -> None:
        """This will pass input to other classses"""
        # HANDLE EVENTS (eg. key press)
        for event in pygame.event.get():
            
            # quit game if is being window closed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle key press
            elif event.type == pygame.KEYDOWN:

                # temporary exit way (escape key)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # mouse press (relise)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_click = True
                self.pos = pygame.mouse.get_pos()

        # Process mouse press
        if self.mouse_click:
            # debugging print
            print(self.state)
            # Unpack mouse position
            x, y = self.pos
            # buy tower
            if 1680 < x < 1800:
                if 960 < y < 1080:
                    if UI.state == "buy tower":
                        UI.state = "idle"
                    else:
                        UI.state = "buy tower"

            elif UI.state == "buy tower":
                tile : Coord = Coord.res2tile(self.pos) 
                # temporary choosen tower
                chosen_tower = "test_tower_1"
                if map.grid[tile.y][tile.x]:
                    if chosen_tower in player.affordable_towers():
                        map.grid[tile.y][tile.x] = False
                        Tower_Manager(chosen_tower, Coord(x, y))
                        player.gold -= Tower.tower_types[chosen_tower][-1]
                        
        self.mouse_click = False

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
                 bullets_names : dict = {"test_bullet" : "bullet_placeholder.png"},
                 number_of_waves : int = 3) -> None:
        # Load graphics
        self.map_gfx = pygame.image.load(os.path.join(self.gfx_path, "maps", map_name + "_map.png"))
        self.towers_gfx = {name : pygame.image.load(os.path.join(self.gfx_path, "towers", file)) 
                           for name, file in towers_names.items()}
        self.bullets_gfx = {name : pygame.image.load(os.path.join(self.gfx_path, "bullets", file))
                            for name, file in bullets_names.items()}  
        self.number_of_waves = number_of_waves
        self.current_wave = 1
    
    def new_wave(self) -> None:
        self.current_wave += 1

    def update(self, gold : int, lives : int) -> None:
        # DRAW ELEMENTS
        # background
        self.screen.blit(self.map_gfx, (0, 0))
        # towers
        for tower in Tower_Manager.towers:
            self.screen.blit(self.towers_gfx["test_tower"], tower.display_pos)
        # HUD
        self.hud(gold, lives)

        # UPDATE SCREEN
        pygame.display.flip()
        self.clock.tick(self.FPS)

    def hud(self, gold : int, lives : int) -> None:
        # player name
        self.screen.blit(self.player_name_gfx, (20, 845))
        # player money
        self.screen.blit(self.font.render(f"Gold:    {gold}", False, (0, 0, 0)), (20, 905))
        # lives
        self.screen.blit(self.font.render(f"Lives:   {lives}", False, (0, 0, 0)), (20, 965))
        # Wave number
        self.screen.blit(self.font.render(f"Wave:    {self.current_wave}/{self.number_of_waves}", False, (0, 0, 0)), (20, 1025))
        # buttons
        buttons_font = pygame.font.SysFont("Consolas", 40)
        # button 1
        self.screen.blit(self.button_gfx, (960, 840))
        # button 2
        self.screen.blit(self.button_gfx, (960, 960))
        # button 3
        self.screen.blit(self.button_gfx, (1200, 840))
        # button 4
        self.screen.blit(self.button_gfx, (1200, 960))
        # button 5
        self.screen.blit(self.button_gfx, (1440, 840))
        # button 6
        self.screen.blit(self.button_gfx, (1440, 960))
        # button 7
        self.screen.blit(self.button_gfx, (1680, 840))
        # button 8 (buy tower)
        self.screen.blit(self.button_gfx, (1680, 960))
        colour = (0, 255, 0) if self.state == "buy tower" else (0, 0, 0)
        buy_tower_txt = buttons_font.render("Buy Tower", False, colour)
        self.screen.blit(buy_tower_txt, (1700, 995))

        
