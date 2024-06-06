"""
This module contains the UI class for managing interactions with the user, 
including input from the keyboard and mouse and drawing graphics (potentially also handling sounds in the future).
"""

# IMPORTS
import pygame, os, sys
from ..Tower.Tower_Classes import Tower_Manager, Tower
from ..Utilities import Coord
from ..Player.Player import Player
from ..Map.Map_Class import Map as mp
from ..Enemy.Enemy import Enemy_Manager

class UI():
    """
    Manages interactions with the user, including input from the keyboard and mouse, and drawing graphics.

    Class Attributes:
        state (dict[str, bool]): Dictionary to hold current information about UI states such as "wave", "buy tower", and "pause".
        FPS (int): The frame rate of the game.
        RESOLUTION (tuple[int, int]): The resolution of the game window.

    Instance Attributes:
        screen (pygame.Surface): The main game display surface.
        clock (pygame.time.Clock): Manages the game's frame rate.
        mouse_click (bool): Tracks the state of mouse clicks.
        pos (tuple[int, int]): Tracks urrent mouse position.
        gfx_path (str): Path to the graphics assets.
        font (pygame.font.Font): Font used for HUD elements.
        hp_font (pygame.font.Font): Font used for enemy health points.
        player_name_gfx (pygame.Surface): Rendered graphic for the player's name.
        button_gfx (pygame.Surface): Graphic for the buttons.
        map_gfx (pygame.Surface): Graphic for the game map.
        towers_gfx (dict): Graphics for the towers.
        bullets_gfx (dict): Graphics for the bullets.
        enemies_gfx (dict): Graphics for the enemies.
        number_of_waves (int): Total number of waves in the current level.
        current_wave (int): The current wave number.

    Methods:
        __init__(player_name: str) -> None: Initializes the UI instance and sets up the display and initial variables.
        
        process_input(map: mp, player: Player) -> None: Processes user input from the keyboard and mouse.
        
        intro() -> None: Displays the intro sequence.
        main_menu() -> bool: Displays the main menu and handles menu interactions.
        outro() -> None: Placeholder for the outro sequence.
        
        update(gold: int, lives: int, enemies: list) -> None: Updates the game display each frame.
        hud(gold: int, lives: int) -> None: Draws the HUD elements on the screen.
        
        load_lvl(number_of_waves: int = 3, current_wave: int = 0, map_name: str = "TEST_1", 
                 towers_names: dict = {"test_tower": "tower_placeholder.png"}, 
                 bullets_names: dict = {"test_bullet": "bullet_placeholder.png"}, 
                 enemies_names: dict = {"test_enemy": "enemy_placeholder.png"}) -> None: 
                 Loads level graphics and initializes level variables.
    """
    # Game state for adjusting what gets displayed and how
    state : dict[str, bool] = {"wave" : False, "buy tower" : False, "pause" : False}
    
    # Constant parameters
    FPS : int = 60 # framerate
    RESOLUTION : tuple[int, int] = 1920, 1080

    # Constructor
    def __init__(self, player_name : str) -> None:
        """
        Initializes the UI class.

        Sets up the game window, initializes utility variables, and loads HUD elements.

        Args:
            player_name (str): The name of the player.
        """
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
        self.hp_font = pygame.font.SysFont("Consolas", 20)
        player_name = player_name if len(player_name) < 20 else player_name[:17] + "..."
        self.player_name_gfx = self.font.render("Player:  " + player_name, False, (0, 0, 0))
        self.button_gfx = pygame.image.load(os.path.join(self.gfx_path, "HUD", "BLANK_BUTTON.png"))

    # Input
    def process_input(self, map : mp, player : Player) -> bool:
        """
        Processes user input from the keyboard and mouse.

        Handles events such as quitting the game, pausing the game, and mouse clicks 
        for interactions like starting a wave, buying a tower, and exiting the game.

        Args:
            map (mp): The current game map.
            player (Player): The player instance.

        Returns:
            bool: True if the game should terminate, False otherwise.
        """
        # HANDLE EVENTS (eg. key press)
        for event in pygame.event.get():
            
            # Quit game if is being window closed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle key press
            elif event.type == pygame.KEYDOWN:

                # Pauses game (still in development)
                if event.key == pygame.K_ESCAPE:
                    pass

            # mouse press (release)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_click = True
                self.pos = pygame.mouse.get_pos()

        # Process mouse press
        # (Spaghetti code, needs restructuring when more options will be programmed)
        if self.mouse_click:
            # debugging print
            #print(self.state)

            # Unpack mouse position
            x, y = self.pos
            if 1680 < x < 1800:
                # buy tower
                if 960 < y < 1080:
                    if UI.state["buy tower"]:
                        UI.state["buy tower"] = False
                    else:
                        UI.state["buy tower"] = True
                # exit
                elif 840 < y < 960:
                    print("Game terminated with a button")
                    return True
                
            if 1440 < x < 1680:
                #start wave
                if 960 < y < 1080:
                    if not UI.state["wave"]:
                        UI.state["wave"] = True

            # Buying tower
            if UI.state["buy tower"]:
                # Cast mouse position to coord type
                tile : Coord = Coord.res2tile(self.pos) 
                # temporary choosen tower, to be changed when more towers are developed
                chosen_tower = "test_tower_1"
                if map.grid[tile.y][tile.x]:
                    if chosen_tower in player.affordable_towers():
                        map.grid[tile.y][tile.x] = False
                        Tower_Manager(chosen_tower, Coord(x, y))
                        player.gold -= Tower.tower_types[chosen_tower][-1]

        # Reset mouse state to not clicked
        self.mouse_click = False

        # Return False to indicate game still runnning 
        return False

    # Menus
    def intro(self) -> None:
        """
        Displays the intro screen with a title animation.

        Writes down the title "Hello World!" character by character in the center 
        of the screen with a delay for a visual effect.

        --- Temporary intro to test functionality ---
        """
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

    def main_menu(self) -> str:
        """
        Displays the main menu and handles user input.

        Returns:
            str:    "start" if the start button is pressed, 
                    "quit" if the quit button is pressed.
        """
        # Load and display background graphic
        main_menu_graphic = pygame.image.load(os.path.join(self.gfx_path, "main_menu.png"))
        self.screen.blit(main_menu_graphic, (0, 0))

        # Main menu loop
        while True:

            # HANDLE EVENTS (eg. key press)
            for event in pygame.event.get():
                
                # Quit game if window is being closed
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Mouse press (relise)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_click = True
                    self.pos = pygame.mouse.get_pos()

            # PROCESS INTERACTION
            if self.mouse_click:
                x, y = self.pos
                if 700 < x < 1300:
                    # Start button pressed
                    if 325 < y < 600:
                        return "start"
                    
                    # Quit button pressed
                    elif 640 < y < 880:
                        return "quit"

            # Update pygame and clock every 60'th of a secound
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def outro(self) -> None:
        """
        Displays the outro screen.

        Placeholder for the outro screen functionality.
        """
        # Write down title character by character on the center of the screen
        font = pygame.font.SysFont('Consolas', 200)
        title = "Have a nice day!"
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

    # In-frame updates
    def update(self, gold : int, lives : int, enemies : list) -> None:
        """
        Updates and renders the game state.

        Draws the game background, towers, enemies, and HUD elements on the screen.
        Updates the display with the current game state.

        Args:
            gold (int): The current amount of gold the player has.
            lives (int): The current number of lives the player has.
            enemies (list): A list of active enemies to display on the screen.
        """
        # DRAW ELEMENTS
        # background
        self.screen.blit(self.map_gfx, (0, 0))

        # towers
        for tower in Tower_Manager.towers:
            self.screen.blit(self.towers_gfx["test_tower"], tower.display_pos)

        # enemies
        if UI.state["wave"]:
            self.enemies : list[Enemy_Manager] = enemies
            for enemy in self.enemies:
                self.screen.blit(self.enemies_gfx[enemy.name], enemy.display_pos)
                enemy.hp_display = self.hp_font.render(f"{enemy.life}", False, (255, 0, 0))
                self.screen.blit(enemy.hp_display, enemy.display_pos)
                if enemy.attacked:
                    self.screen.blit(self.bullets_gfx["test_bullet"], enemy.display_pos)

        # HUD
        self.hud(gold, lives)

        # UPDATE SCREEN
        pygame.display.flip()
        self.clock.tick(self.FPS)

    def hud(self, gold : int, lives : int) -> None:
        """
        Displays the HUD (heads-up display) elements on the screen.

        Renders the player's name, gold, lives, wave number, and action buttons on the HUD.

        Args:
            gold (int): The current amount of gold the player has.
            lives (int): The current number of lives the player has.
        """
        # Player name
        self.screen.blit(self.player_name_gfx, (20, 845))
        # Player money
        self.screen.blit(self.font.render(f"Gold:    {gold}", False, (0, 0, 0)), (20, 905))
        # Lives
        self.screen.blit(self.font.render(f"Lives:   {lives}", False, (0, 0, 0)), (20, 965))
        # Wave number
        self.screen.blit(self.font.render(f"Wave:    {self.current_wave}/{self.number_of_waves}", False, (0, 0, 0)), (20, 1025))
        
        # Buttons
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

        # button 6 (start wave)
        self.screen.blit(self.button_gfx, (1440, 960))
        colour = (0, 255, 0) if self.state["wave"] else (0, 0, 0)
        start_wave_txt = buttons_font.render("Start Wave", False, colour)
        self.screen.blit(start_wave_txt, (1450, 995))

        # button 7 (exit)
        self.screen.blit(self.button_gfx, (1680, 840))
        exit_txt = buttons_font.render("EXIT", False, (255, 0, 0))
        self.screen.blit(exit_txt, (1755, 880))

        # button 8 (buy tower)
        self.screen.blit(self.button_gfx, (1680, 960))
        colour = (0, 255, 0) if self.state["buy tower"] else (0, 0, 0)
        buy_tower_txt = buttons_font.render("Buy Tower", False, colour)
        self.screen.blit(buy_tower_txt, (1700, 995))

    # Additional methods
    def load_lvl(self, 
                 number_of_waves : int = 3,
                 current_wave : int = 0 ,
                 map_name : str = "TEST_1", 
                 towers_names : dict = {"test_tower" : "tower_placeholder.png"},
                 bullets_names : dict = {"test_bullet" : "bullet_placeholder.png"},
                 enemies_names : dict = {"test_enemy" : "enemy_placeholder.png"}) -> None:
        """
        Loads the game level with specified parameters.

        Initializes graphics for the map, towers, bullets, and enemies. Sets the number of waves 
        and the current wave number.

        Args:
            number_of_waves (int): Total number of waves in the level. Defaults to 3.
            current_wave (int): The current wave number. Defaults to 0.
            map_name (str): The name of the map. Defaults to "TEST_1".
            towers_names (dict): Dictionary of tower names and their corresponding file names. Defaults to {"test_tower": "tower_placeholder.png"}.
            bullets_names (dict): Dictionary of bullet names and their corresponding file names. Defaults to {"test_bullet": "bullet_placeholder.png"}.
            enemies_names (dict): Dictionary of enemy names and their corresponding file names. Defaults to {"test_enemy": "enemy_placeholder.png"}.
        """
        # Load graphics
        self.map_gfx = pygame.image.load(os.path.join(self.gfx_path, "maps", map_name + "_map.png"))
        self.towers_gfx = {name : pygame.image.load(os.path.join(self.gfx_path, "towers", file)) 
                           for name, file in towers_names.items()}
        self.bullets_gfx = {name : pygame.image.load(os.path.join(self.gfx_path, "bullets", file))
                            for name, file in bullets_names.items()}  
        self.enemies_gfx = {name : pygame.image.load(os.path.join(self.gfx_path, "enemies", file))
                            for name, file in enemies_names.items()}
        self.number_of_waves = number_of_waves
        self.current_wave = current_wave + 1

        
