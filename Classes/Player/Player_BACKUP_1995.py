from Classes.Tower.Tower_Classes import Tower

class Player: # Defines the player entity

    def __init__(self, name : str, gold : int, lives : int, avtw : list[str]) -> None:
        self.name = name
        self.gold = gold
        self.lives = lives
        self.avialable_towers = avtw

    def affordable_towers(self) -> list[str]:
        """Returns which of the towers available on the level are affordable"""
        affordable=[]
        for tower in self.avialable_towers:
            if Tower.tower_types[tower][-1] <= self.gold:
               affordable.append(tower) 
        return affordable
    def deduct_lives(self):
        self.lives -=1
