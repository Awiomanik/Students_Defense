"""
"""

# IMPORTS
from ..UI import UI
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

        # DISPLAY INTRO
        if display_intro:
            self.ui.intro()

        # DISPLAY MAIN MENU
        self.ui.main_menu()

        # LOAD LEVEL
        self.ui.load_lvl()

        # Main gameplay loop
        running = True
        while running:
            # player 
            # other classes exchange information
            self.ui.update()


if __name__ == "__main__":
    Game(False)

