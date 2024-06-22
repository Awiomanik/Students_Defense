from Classes.Tower.Tower_Classes import Tower

class Player: # Defines the player entity
    """
    Defines the player entity and manages player attributes and actions.

    Instance Atributes:
    name (str): The name of the player.
    gold (int): The amount of gold the player has
    lives (int): The number of lives the player has.
    available_towers (list[str]):  A list of tower types that are available to the player.


    Methods:
    __init__(self, name : str, gold : int, lives : int, avtw : list[str]) -> None
        Initializes a player with the given name, gold, lives, and available towers.

    affordable_towers(self) -> list[str]:
        Returns a list of towers that the player can afford based on their current gold.

    deduct_lives(self):
        Decreases the player's lives by one.

    """

    def __init__(self, name : str, gold : int, lives : int) -> None:
        """ Initializes a player with the given name, gold, lives, and available towers.
         
            Arguments:
            name : str, gold : int, lives : int
          
        """
        self.name = name
        self.gold = gold
        self.lives = lives

    def affordable_towers(self) -> list[str]:
        """Returns which of the towers available on the level are affordable"""
        affordable=[]
        for tower in Tower.tower_types.keys():
            if Tower.tower_types[tower][7] <= self.gold:
               affordable.append(tower) 
        return affordable
    
    def deduct_lives(self):
        """Decreases the player's lives by one."""
        self.lives -=1
