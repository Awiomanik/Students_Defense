"""
This module contains the UI class for managing interactions with the user, 
including input from the keyboard and mouse and drawing graphics (potentially also handling sounds in the future).
"""

# IMPORTS
import pygame
import os
import sys
from ..Tower.Tower_Classes import Tower_Manager, Tower
from ..Utilities import Coord, InputBox, load_high_scores, xor
from ..Player.Player import Player
from ..Map.Map_Class import Map as mp
from ..Enemy.Enemy import EnemyManager

class UI():
    """
    Manages interactions with the user, including input from the keyboard and mouse, and drawing graphics.

    Class Attributes:
        state (dict[str, bool]): Dictionary to hold current information about UI states such as "wave", "buy tower", "speed up" and "pause".
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
        buttons (dict[str, pygame.Surface]): Dictionary of button images for UI. (Keys include: "exit", "ff_NA", "ff_off", "ff", "ff_2", "pause", "play")
        map_gfx (pygame.Surface): Graphic for the game map.
        towers_gfx (dict): Graphics for the towers.
        towers_list (list): List of tower_gfx keys, ie. list of towers that player can buy in currrent level.
        towers_HUD_gfx (dict) : Graphics for towers displayed in HUD (corresponding to towers_list and towers_gfx).
        bullets_gfx (dict): Graphics for the bullets.
        enemies_gfx (dict): Graphics for the enemies.
        number_of_waves (int): Total number of waves in the current level.
        current_wave (int): The current wave number.
        directory (str): Path to the root directory of the repository.
        frame_counter (int): Current frame (not absolute) for speeding up the game by ommiting some frames.
        tower_bieing_bought (int): Index of tower currently being bought (defaults to -1).

    Methods:
        __init__(player_name: str) -> None: Initializes the UI instance and sets up the display and initial variables.
        
        process_input(map: mp, player: Player) -> None: Processes user input from the keyboard and mouse.
        
        intro() -> None: Displays the intro sequence.
        main_menu() -> bool: Displays the main menu and handles menu interactions.
        outro() -> None: Placeholder for the outro sequence.
        
        update(gold: int, lives: int, enemies: list) -> None: Updates the game display each frame.
        hud(gold: int, lives: int, map : mp) -> None: Draws the HUD elements on the screen.
        
        load_lvl(number_of_waves: int = 3, current_wave: int = 0, map_name: str = "TEST_1", 
                 towers_names: dict = {"test_tower": "tower_placeholder.png"}, 
                 bullets_names: dict = {"test_bullet": "bullet_placeholder.png"}, 
                 enemies_names: dict = {"test_enemy": "enemy_placeholder.png"}) -> None: 
                 Loads level graphics and initializes level variables.

        reset_state(cls) -> None: Resets state dict keys to all False

        skip_frames(self, num_of_frames_2_skip : int) -> bool: Determines if the frame should be displayed or skipped based on the speed up states.

        accessibility_rectangle(self, tile_size : int, map : mp) -> bool:   Checks if a position on the game map, based on the current mouse position, 
                                                                            is suitable for placing a tower and visually indicates this with a colored rectangle.
    """
    # Game state for adjusting what gets displayed and how
    state : dict[str, bool] = {key: False for key in 
                               ["wave", "buy tower", "pause", "speed up", "speed up more"]}
    """State includes: 'wave', 'buy tower', 'pause', 'speed up', 'speed up more'"""
    
    # Constant parameters
    FPS : int = 60 # framerate
    RESOLUTION : tuple[int, int] = 1920, 1080

    # Constructor
    def __init__(self, root_directory : str) -> None:
        """
        Initializes the UI class.

        Sets up the game window, initializes utility variables, and loads HUD elements.

        Args:
            root_directory (str): Path to the main calogue f the repository for relative path operations.
        """
        # SET UP WONDOW AND PYGAME
        # initialize Pygame
        pygame.init()
        # set up the full-screen mode and resolution
        self.screen : pygame.Surface = pygame.display.set_mode(self.RESOLUTION, pygame.FULLSCREEN)
        # set the title of the window
        pygame.display.set_caption("STUDENTS DEFENSE")

        # INITIALIZE UTILITY VARIABLES
        # variable for menaging frame rate
        self.clock : pygame.time.Clock = pygame.time.Clock() 
        # varibles for menaging user mouse input
        self.mouse_click : bool = False 
        self.pos : tuple = pygame.mouse.get_pos()

        # SET ASSETS PATHS
        self.gfx_path : str = os.path.join(root_directory, "Assets", "gfx")
        # audio path (in the future)

        # SET AND LOAD HUD ELEMENTS
        self.font : pygame.font.Font = pygame.font.SysFont("Consolas", 50)
        self.hp_font : pygame.font.Font = pygame.font.SysFont("Consolas", 20)

        # Button graphics
        # File names
        file_names = ["Exit.png", "Fast_forward_NA.png", 
                      "Fast_forward_Off.png", "Fast_forward_On.png", 
                      "Fast_forward_On_2.png", "Pause.png", "Play.png"]
        # Keys
        keys = ["exit", "ff_NA", "ff_off", "ff", "ff_2", "pause", "play"]
        # Button images dict
        self.buttons : dict = {key : pygame.image.load(os.path.join(self.gfx_path, "HUD", button))
                                for key, button in zip(keys, file_names)}
        self.buttons_L : dict = {key : pygame.image.load(os.path.join(self.gfx_path, "HUD", "HUD_L", button))
                                    for key, button in zip(keys, file_names)}
        """Buttons include: 'exit', 'ff_NA', 'ff_off', 'ff', 'ff_2', 'pause', 'play'"""

        # Save root directory to an atribute
        self.directory : str = root_directory

        # Frame counter for speeding up the displaying the game
        self.frame_counter : int = 0

        # Default value for currently being bought tower
        self.tower_being_bought : int = -1

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
            # Click at HUD (below map)
            if y > 860:

                # Exit button
                if x > 1700:
                    return True
                
                # Play/Pause button
                if x > 1460:
                    # If wave did not start yet, start it
                    if not UI.state["wave"]:
                        UI.state["wave"] = True
                    # If wave currently marching
                    else:
                        # Reverse pause state
                        UI.state["pause"] = not UI.state["pause"]

                # Speed up button
                elif x > 1220:
                    if self.state["speed up"]:
                        self.state["speed up"] = False
                        self.state["speed up more"] = True
                    elif self.state["speed up more"]:
                        self.state["speed up more"] = False
                    elif self.state["wave"]:
                        self.state["speed up"] = True

                # Towers (HUD)
                elif x > 980:
                  self.buy_tower_mode(2, player)
                elif x > 740:
                    self.buy_tower_mode(1, player)
                elif x > 500:
                    self.buy_tower_mode(0, player)

            # Click at map
            else:
                # Place tower
                if self.state["buy tower"]:
                    # Cast mouse position to coord type
                    tile : Coord = Coord.res2tile(self.pos) 

                    # temporary choosen tower, to be changed when more towers are developed
                    if map.grid[tile.y][tile.x]:
                        chosen_tower = self.towers_list[self.tower_being_bought]
                        map.grid[tile.y][tile.x] = False
                        Tower_Manager(chosen_tower, Coord(x, y))
                        player.gold -= Tower.tower_types[chosen_tower][7]

        # Reset mouse state to not clicked
        self.mouse_click = False

        # Return False to indicate game still runnning 
        return False

    # Menus
    def intro(self) -> None:
        """

        MARTA, JAKBYS MIALA JAKIES PYTANIA PISZ ;) WOJTEK

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

    def main_menu(self, player : Player) -> str:
        """
        Displays the main menu and handles user input, 
        that includes changing users name displaying high scores 
        or returnin a string informing starting a game or quiting.

        Args:
            player (Player): Player instance for player name access.

        Returns:
            str:    "start" if the start button is pressed, 
                    "quit" if the quit button is pressed
        """
        # Load background graphic
        main_menu_graphic = pygame.image.load(os.path.join(self.gfx_path, "menu", "Menu.png"))

        # Main menu loop
        while True:
            
            # Display background graphic
            self.screen.blit(main_menu_graphic, (0, 0))
            # Display player name
            self.screen.blit(self.font.render(f"Player name: {player.name}", False, (100, 0, 0)), (150, 960))

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
                # Play and quit buttons
                if 840 < x < 1080:
                    # Demo button pressed
                    if 180 < y < 324:
                        return "start"
                    
                    # Quit button pressed
                    elif 504 < y < 648:
                        return "quit"
                
                # Name change and High Scores
                elif 1400 < x < 1800:
                    if 940 < y < 1015:
                        player.name = self.handle_name_change(player.name, main_menu_graphic)
                        
                    # High Scores
                    elif x > 1550:
                        if 725 < y < 875:
                            self.high_scores()
                
            self.mouse_click = False
                
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

    def high_scores(self) -> None:
        """
        Displays High Scores.

        Loads High Scores from file and displays them.
        Waits for user to exit back to main menu vie ESCAPE button press.
        """
        # Get data
        hs = load_high_scores(self.directory)
        # Initialize length of displayed records
        records_width = 45

        # Blit background image
        self.screen.blit(pygame.image.load(os.path.join(self.gfx_path, 
                                                        "menu", "high_scores_background.png")), 
                                                            (0, 0))

        # Blit exit instructions
        self.screen.blit(self.font.render("Press escape to exit High Scores", False, (50, 50, 50)), (570, 180))

        # Blit records
        x, y = 300, 260
        for i, record in enumerate(hs[:10], 1):
            num, num_len = (str(i) + ".  ", 3) if i != 10 else ("10. ", 4)
            formatted_record = num + \
                               record[0] + \
                               '.' * (records_width - len(record[0] + str(record[1]) + str(i)) + num_len) + \
                               str(record[1])
            self.screen.blit(self.font.render(formatted_record, False, (255, 255, 0)), (x, y))
            y += 70

        # Update display
        pygame.display.flip()

        # Wait for user to exit High Scores using ESCAPE key
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False

    # In-frame updates
    def update(self, gold : int, lives : int, enemies : list, map : mp) -> None:
        """
        Updates and renders the game state.

        Draws the game background, towers, enemies, and HUD elements on the screen.
        Updates the display with the current game state.

        Args:
            gold (int): The current amount of gold the player has.
            lives (int): The current number of lives the player has.
            enemies (list): A list of active enemies to display on the screen.
        """
        # If speed up (speed up more) state active, ommit every three (four) out of four (five) frames
        if UI.state["speed up"]:
            if self.skip_frames(3):
                return 
        
        elif UI.state["speed up more"]:
            if self.skip_frames(8):
                return

        # DRAW ELEMENTS
        # background
        self.screen.blit(self.map_gfx, (0, 0))

        # towers
        for tower in Tower_Manager.towers:
            self.screen.blit(self.towers_gfx[tower.tower_type.tower_asset[:-4]], tower.display_pos)

        # enemies
        if UI.state["wave"]:
            self.enemies : list[EnemyManager] = enemies
            for enemy in self.enemies:
                self.screen.blit(self.enemies_gfx[enemy.name], enemy.display_pos)
                enemy.hp_display = self.hp_font.render(f"{enemy.life}", False, (255, 0, 0))
                self.screen.blit(enemy.hp_display, enemy.display_pos)
                if enemy.attacked:
                    self.screen.blit(self.bullets_gfx["test_bullet"], enemy.display_pos)

        # HUD
        self.hud(gold, lives, map)

        # UPDATE SCREEN
        pygame.display.flip()
        self.clock.tick(self.FPS)

    def hud(self, gold : int, lives : int, map : mp) -> None:
        """
        Displays the HUD (heads-up display) elements on the screen.

        Renders the player's name, gold, lives, wave number, and action buttons on the HUD.

        Args:
            gold (int): The current amount of gold the player has.
            lives (int): The current number of lives the player has.
            map (Map): reference to map object for checking accessibility of tiles for tower placement.
        """
        # Update mouse position and check if mouse is hovering upon any button
        x, y = self.pos = pygame.mouse.get_pos()
        hover = None
        if y > 860:
            # Exit button
            if x > 1700:
                hover = "exit"
            # Play/Pause button
            elif x > 1460:
                hover = "play"
            # Speed up button
            elif x > 1220:
                hover = "speed up"
            # Towers
            elif x > 980:
                hover = "tower 2"
            elif x > 740:
                hover = "tower 1"
            elif x > 500:
                hover = "tower 0"

        # Player name
        self.screen.blit(self.player_name_gfx, (20, 845))
        # Player money
        self.screen.blit(self.font.render(f"Gold:    {gold}", False, (0, 0, 0)), (20, 905))
        # Lives
        self.screen.blit(self.font.render(f"Lives:   {lives}", False, (0, 0, 0)), (20, 965))
        # Wave number
        self.screen.blit(self.font.render(f"Wave:    {self.current_wave}/{self.number_of_waves}", False, (0, 0, 0)), (20, 1025))
        
        # Buttons
        # Exit
        if hover == "exit":
            self.screen.blit(self.buttons_L["exit"], (1700, 860))
        else:
            self.screen.blit(self.buttons["exit"], (1710, 870))

        # Play / Pause
        if self.state["wave"] and not self.state["pause"]:
            temp_key = "pause"
        else:
            temp_key = "play"
        if hover == "play":
            self.screen.blit(self.buttons_L[temp_key], (1460, 860))
        else:
            self.screen.blit(self.buttons[temp_key], (1470, 870))

        # Speed
        but = self.buttons_L if hover == "speed up" else self.buttons
        position = (1220, 860) if hover == "speed up" else (1230, 870)
        if self.state["wave"]:
            if self.state["speed up"]:
                button_helper = but["ff"]
            elif self.state["speed up more"]:
                button_helper = but["ff_2"]
            else:
                button_helper = but["ff_off"]
        else:
            button_helper = but["ff_NA"]
        # Blit proper button
        self.screen.blit(button_helper, position)

        # Towers - HUD
        # Left
        if hover == "tower 0":
            self.screen.blit(self.towers_HUD_gfx_L[self.towers_list[0]], (500, 860))
        else:
            self.screen.blit(self.towers_HUD_gfx[self.towers_list[0]], (510, 870))
        # Center ( PLACEHOLDER, Add new towers )
        if hover == "tower 1":
            self.screen.blit(self.towers_HUD_gfx_L[self.towers_list[1]], (740, 860))
        else:
            self.screen.blit(self.towers_HUD_gfx[self.towers_list[1]], (750, 870))
        # Riht ( PLACEHOLDER, Add new towers)
        if hover == "tower 2":
            self.screen.blit(self.towers_HUD_gfx_L[self.towers_list[2]], (980, 860))
        else:
            self.screen.blit(self.towers_HUD_gfx[self.towers_list[2]], (990, 870))
        
        # Placing towers
        if self.state["buy tower"]:
            self.pos = pygame.mouse.get_pos()
            self.accessibility_rectangle(120, map)

    # Additional methods
    def load_lvl(self, 
                 player_name : str = "Guest",
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
            player_name (str): Players name to display in HUD.
            number_of_waves (int): Total number of waves in the level. Defaults to 3.
            current_wave (int): The current wave number. Defaults to 0.
            map_name (str): The name of the map. Defaults to "TEST_1".
            towers_names (dict): Dictionary of tower names and their corresponding file names. Defaults to {"test_tower": "tower_placeholder.png"}.
            bullets_names (dict): Dictionary of bullet names and their corresponding file names. Defaults to {"test_bullet": "bullet_placeholder.png"}.
            enemies_names (dict): Dictionary of enemy names and their corresponding file names. Defaults to {"test_enemy": "enemy_placeholder.png"}.
        """
        # Load graphics
        self.map_gfx = pygame.image.load(os.path.join(self.gfx_path, "maps", f"{map_name}.png"))
        self.towers_gfx : dict = {name : pygame.image.load(os.path.join(self.gfx_path, "towers", file)) 
                                    for name, file in towers_names.items()}
        self.towers_gfx_L : dict = {name : pygame.image.load(os.path.join(self.gfx_path, "HUD", "HUD_L", file)) 
                                    for name, file in towers_names.items()}
        self.towers_list : list = [name for name in self.towers_gfx.keys()]
        self.towers_HUD_gfx : dict = {name : pygame.image.load(os.path.join(self.gfx_path, "HUD", file)) 
                                        for name, file in towers_names.items()}
        self.towers_HUD_gfx_L : dict = {name : pygame.image.load(os.path.join(self.gfx_path, "HUD", "HUD_L", file)) 
                                        for name, file in towers_names.items()}
        self.bullets_gfx : dict = {name : pygame.image.load(os.path.join(self.gfx_path, "bullets", file))
                                    for name, file in bullets_names.items()}  
        self.enemies_gfx : dict = {name : pygame.image.load(os.path.join(self.gfx_path, "enemies", file))
                                    for name, file in enemies_names.items()}
        
        self.number_of_waves = number_of_waves
        self.current_wave = current_wave + 1
        player_name = player_name if len(player_name) < 20 else player_name[:17] + "..."
        self.player_name_gfx = self.font.render("Player:  " + player_name, False, (0, 0, 0))

    def handle_name_change(self, current_player_name : str, background : pygame.image) -> str:
        """
        Displays input box for user to input new name and updates it live while user is typing.

        Parameters:
            current_player_name (str) : Current name of the player to display at the beggining.

        Returns:
            str - New user name.
        """
        input = InputBox(500, 955, 500, 60, 
                        current_player_name, display_box=True, 
                        font=self.font, activate=True)
        clock = pygame.time.Clock()

        typing = True
        while typing:
            # Exit via closing the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    typing = False

                # Key press
                elif event.type == pygame.KEYDOWN:

                    # Exit via ESCAPE or ENTER key press
                    if event.key == pygame.K_ESCAPE or \
                    event.key == pygame.K_RETURN:
                        typing = False

                input.handle_event(event)
                # Check if box deactivated (via mouse click o carrige return key press)
                if not input.active:
                    typing = False

            self.screen.blit(background, (0, 0))
            self.screen.blit(self.font.render(f"Player name:", False, (100, 0, 0)), (150, 960))
            input.draw(self.screen)
            pygame.display.flip()
            clock.tick(30)

        return input.text

    @classmethod
    def reset_state(cls) -> None:
        """Resets state dict to all False"""
        cls.state = {key : False for key in cls.state.keys()}

    def skip_frames(self, num_of_frames_2_skip : int) -> bool:
        """
        The method increments an internal frame counter each time it is called. If the counter is less than 
        `num_of_frames_2_skip`, the function will return True, indicating the frame should be skipped. Once the counter 
        reaches `num_of_frames_2_skip`, it is reset to zero and the function returns False, indicating the frame 
        should not be skipped and processing should take place.

        Parameters:
        num_of_frames_2_skip (int): The number of frames to skip before processing a frame. This value determines
                                    how frequently the frames are processed (e.g., if set to 3, every 4th frame 
                                    will be processed).

        Returns:
        bool: Returns True if the current frame should be skipped, False if it should be processed.
        """
        self.frame_counter += 1
        # Ommit frame three times out of four
        if self.frame_counter < num_of_frames_2_skip:
            return True
        # Fourth frame, restart frame counter and execute the function
        self.frame_counter = 0
        return False
    
    def buy_tower_mode(self, tower_num : int, player : Player) -> None:
        """"""
        if self.state["buy tower"]:
            # Turn off buing tower mode
            if self.tower_being_bought == tower_num:
                self.state["buy tower"] = False

            # Change tower to buy
            elif self.towers_list[self.tower_being_bought] in player.affordable_towers():
                self.tower_being_bought = tower_num

        # Turn on buying tower mode
        elif self.towers_list[self.tower_being_bought] in player.affordable_towers():
            self.state["buy tower"] = True
            self.tower_being_bought = tower_num

    def accessibility_rectangle(self, tile_size : int, map : mp) -> bool:
        """
        Checks if a position on the game map, based on the current mouse position, is suitable for placing a tower and visually indicates this with a colored rectangle.

        Parameters:
        tile_size (int): The size of each tile on the map, used to calculate the exact tile position from the mouse coordinates.
        map (Map): The game map object that contains the tile accessibility information.

        Returns:
        bool:   Returns True if the tile at the mouse position is accessible for placing a tower, otherwise False. 
                If the mouse position is outside the main map area, it also returns False.

        Side Effects:
        Draws a semi-transparent rectangle on the game screen at the tile position of the mouse, indicating whether a tower can be placed there. 
        """
        x, y = self.pos
        # check if mouse position within map
        if y < 860:
            # Check if tower placement possible
            accessible = map.tile_accessibility(Coord.res2tile(self.pos, tile_size))
            color = (255, 0, 0, 150) if accessible else (0, 255, 0, 100)
            x, y = x - x % tile_size, y - y % tile_size 

            # Create a new temporary surface with per-pixel alpha
            path_cut = (tile_size//8)
            path_size = tile_size - 2 * path_cut
            temp_surface = pygame.Surface((path_size, path_size), pygame.SRCALPHA)
            temp_surface.fill((0, 0, 0, 0))  # Fill the surface with a fully transparent color

            # Draw a rounded rectangle on the temporary surface
            pygame.draw.rect(temp_surface, color, 
                            pygame.Rect(0, 0, path_size, path_size), 
                            border_radius=int(tile_size / 5))  # Adjust border radius here

            # Draw the temporary surface onto the main screen at the specified position
            self.screen.blit(temp_surface, (x + path_cut, y + path_cut))

            return accessible

        return False










