"""
"""

# IMPORTS
from ..UI import UI
from ..Level import Test_Level
from ..Player import Player
from ..Tower.Tower_Classes import Tower_Manager

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
        self.level = Test_Level.Level(1)
        self.ui.load_lvl(self.level.waves_num,self.level.current_wave)
        self.player = Player.Player(player_name, 
                                    self.level.gold, 
                                    self.level.lives, 
                                    self.level.available_towers)


        # MAIN GAMEPLAY LOOP
        running = True
        while running:
            self.ui.get_input(self.level.map, self.player)
            if self.ui.state == "wave":
                self.ui.update(self.player.gold, self.player.lives,self.level.enemies)
                #print(self.level.enemies)
                #print(self.level.remaining_enemies)
                self.level.update()
                Tower_Manager.update()
                if not self.level.remaining_enemies and not self.level.enemies:
                    self.ui.get_idle()
                    self.ui.new_wave()
                    if self.level.current_wave<self.level.waves_num - 1:
                        self.level.new_wave()
                    #print('obecnie',self.ui.state)
            else:
                self.ui.update(self.player.gold, self.player.lives,[])


if __name__ == "__main__":
    Game(False)
