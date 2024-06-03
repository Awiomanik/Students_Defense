"""
"""

# IMPORTS
from ..UI import UI
from ..Level import Test_Level
from ..Player import Player
from ..Tower import Tower_Classes
from ..Utilities import Coord


class Game():
    """
    This class will menage the whole game instance
    """

    def __init__(self, display_intro : bool = True) -> None:
        """
        """

        # INITIALIZE HELPER CLASSES
        self.ui = UI.UI()
        self.towers = Tower_Classes.Tower_Manager() # what are thoose arguments ???
        self.player = Player.Player("Player_name_placeholder", 1000, self.towers)
        self.level = Test_Level.Level(1)
        # enemies menager

        # DISPLAY INTRO
        if display_intro:
            self.ui.intro()

        # DISPLAY MAIN MENU
        self.ui.main_menu()

        # LOAD LEVEL
        self.ui.load_lvl()
        self.level.start_level()

        # Main gameplay loop
        running = True
        while running:
            # ui get input
            # enemy menager
            # towwer menager
            # player 
            # level update
            self.ui.update()


if __name__ == "__main__":
    Game(False)

