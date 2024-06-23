"""
This module manages the main game loop and integrates various components of the
Students Defense Game project.

Classes:
    Game - Manages the entire game instance including UI, player, and level interactions.
"""

# IMPORTS
from ..UI import UI
from ..Level import Test_Level
from ..Player.Player import Player
from ..Tower.Tower_Classes import Tower_Manager, Tower
from ..Enemy.Enemy import Enemy

class Game():
    """
    Manages the entire game instance including UI, player, and level interactions.

    Attributes:
        ui (UI): An instance of the UI class for managing the user interface.
        player (Player): An instance of the Player class representing the player.
        level (Level): An instance of the Level class representing the game level, including map class instance.
        root_directory (str): Directory in which the main script was called for easy relative path operations.

    Methods:
        __init__(display_intro: bool = True): Initializes the Game instance, sets up UI, displays intro, shows main menu, loads level, and starts the main gameplay loop.
        main_menu(): Displays the main menu.
        load_level(player_name: str): Loads the game level and initializes player.
        gameplay(): Manages the main gameplay loop, updates game state, and handles wave progression.
    """

    def __init__(self, root_directory : str, display_intro : bool = True, display_outro : bool = True) -> None:
        """
        Initializes the Game instance.

        This method sets up the player, UI, displays the intro if specified,
        shows the main menu, loads the level, and starts the main gameplay loop.

        Args:
            root_directory (str): Path to the main calogue f the repository for relative path operations.
            display_intro (bool): Whether to display the intro screen. Defaults to True.
            display_outro (bool): Whether to display the outro screen. Defaults to True.
        """
        # Player protoplast with placeholder atributes, player is fully initialized when level start
        self.player = Player("Guest", 0, 0)

        # Set root_directory
        self.root_directory = root_directory

        # INITIALIZE HELPER CLASSES
        self.ui = UI.UI(self.root_directory)

        # DISPLAY INTRO
        if display_intro:
            self.ui.intro()

        running = True
        while running:

            # DISPLAY MAIN MENU
            if self.main_menu():

                # LOAD LEVEL
                self.load_level()

                # MAIN GAMEPLAY LOOP
                self.gameplay()

            else:
                running = False
        
        # DISPLAY OUTRO
        if display_outro:
            self.ui.outro()

    def main_menu(self) -> bool:
        """
        Displays the main menu.

        This method calls the UI class to display the main menu screen.

        Returns:
            False for exiting the game True otherwise

        Raises:
            Value error - When ui.main_menu method returns unknown value
        """
        choosen_option = self.ui.main_menu(self.player)

        if choosen_option == "start":
            return True

        elif choosen_option == "quit":
            return False

        else:
            raise ValueError(f"ui.main_manu method returned unknown value: {choosen_option}")

    def load_level(self) -> None:
        """
        Loads the game level.

        This method initializes the game level, updates the UI with level information,
        and player atributes with initial game parameters.
        """
        # Reset towers
        Tower_Manager.reset()
        # Initialize level
        Test_Level.Level.reset()
        self.level = Test_Level.Level("TEST", self.root_directory)

        # Load level data to UI
        self.ui.reset_state()
        self.ui.load_lvl(self.player.name, self.level.waves_num, 
                         self.level.current_wave, self.level.map.name, 
                         enemies_names={name : name + ".png" for name in Enemy.enemy_types})
        
        # Update player atributes based on level data
        self.player.gold = self.level.gold
        self.player.lives = self.level.lives

    def gameplay(self) -> None:
        """
        Manages the main gameplay loop.

        This method continuously updates the game state by processing user input,
        updating the UI, and advancing the game level and other game elements. 
        It handles wave progression and tower management within the game loop.
        """
        # main update loop (iterates over frames)
        running = True
        while running:
            # Process input
            if self.ui.process_input(self.level.map, self.player):
                running = False
            
            # wave is running
            elif self.ui.state["wave"] and not self.ui.state["pause"]:
                # Update game elements
                self.level.update()
                Tower_Manager.update()

                # if wave ended
                if not self.level.remaining_enemies and not self.level.enemies:
                    self.ui.state["wave"] = False
                    self.ui.current_wave += 1
                    
                    # level not ended yet
                    if self.level.current_wave < self.level.waves_num - 1:
                        self.level.new_wave()

                    # Level ended ( to be changed, temporary solution for prototype )
                    else:
                        running = False

            
            self.ui.update(self.player.gold, self.player.lives, self.level.enemies, self.level.map)

# For testing
if __name__ == "__main__":
    Game(False)
