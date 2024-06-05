"""
"""

# IMPORTS
from ..UI import UI
from ..Level import Test_Level
from ..Player import Player


class Game():
    """
    This class will menage the whole game instance

    Atributes:
        ui
        player
        level
    """

    def __init__(self, display_intro : bool = True) -> None:
        """
        """
        player_name = "Player_name_placeholder"


        # INITIALIZE HELPER CLASSES
        self.ui = UI.UI(player_name)


        # DISPLAY INTRO
        if display_intro:
            self.ui.intro()


        # DISPLAY MAIN MENU
        self.ui.main_menu()


        # LOAD LEVEL
        self.ui.load_lvl()
        self.level = Test_Level.Level(1)
        self.player = Player.Player(player_name, 
                                    self.level.gold, 
                                    self.level.lives, 
                                    self.level.available_towers)


        # MAIN GAMEPLAY LOOP
        running = True
        while running:
            self.ui.get_input(self.level.map, self.player)
            self.ui.update(self.player.gold, self.player.lives)


if __name__ == "__main__":
    Game(False)

