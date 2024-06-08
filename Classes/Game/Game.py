"""
This module manages the main game loop and integrates various components of the
Students Defense Game project.

Classes:
    Game - Manages the entire game instance including UI, player, and level interactions.
"""

# IMPORTS
from ..UI import UI
from ..Level import Test_Level
from ..Player import Player
from ..Tower.Tower_Classes import Tower_Manager

class Game():
    """
    Manages the entire game instance including UI, player, and level interactions.

    Attributes:
        ui (UI): An instance of the UI class for managing the user interface.
        player (Player): An instance of the Player class representing the player.
        level (Level): An instance of the Level class representing the game level, including map class instance.

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
        player_name = "Player_name_placeholder"

        # INITIALIZE HELPER CLASSES
        self.ui = UI.UI(player_name, root_directory)

        # DISPLAY INTRO
        if display_intro:
            self.ui.intro()

        running = True
        while running:

            # DISPLAY MAIN MENU
            if self.main_menu():

                # LOAD LEVEL
                self.load_level(player_name, root_directory)

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
        """
        choosen_option = self.ui.main_menu()

        if choosen_option == "start":
            pass

        if choosen_option == "quit":
            return False
        
        return True

    def load_level(self, player_name : str, root_directory : str) -> None:
        """
        Loads the game level.

        This method initializes the game level, updates the UI with level information,
        and creates the player instance with initial game parameters.

        Args:
            player_name (str): The name of the player.
            root_directory (str): Path to the main calogue f the repository for relative path operations.
        """
        self.level = Test_Level.Level(1, root_directory)
        self.ui.load_lvl(self.level.waves_num,self.level.current_wave)
        self.player = Player.Player(player_name, 
                                    self.level.gold, 
                                    self.level.lives, 
                                    self.level.available_towers)

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

            # Update game elements
            if self.ui.state["wave"]:
                self.ui.update(self.player.gold, self.player.lives, self.level.enemies)
                self.level.update()
                Tower_Manager.update()
                # if wave ended
                if not self.level.remaining_enemies and not self.level.enemies:
                    self.ui.state["wave"] = False
                    self.ui.current_wave += 1
                    # 
                    if self.level.current_wave < self.level.waves_num - 1:
                        self.level.new_wave()
                    # Level ended ( to be changed, temporary solution for prototype )
                    else:
                        running = False
            else:
                self.ui.update(self.player.gold, self.player.lives,[])


# For testing
if __name__ == "__main__":
    Game(False)
