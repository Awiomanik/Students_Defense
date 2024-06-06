import Classes.Tower.Tower_Classes as tw

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
            if tw.Tower.tower_types[tower][-1] <= self.gold:
               affordable.append(tower) 
        return affordable

    def place_tower(self, tower: tw.Tower, x: int, y: int) -> bool:
        if  tower in self.affordable_towers():
            print("You cannot afford this tower.")
            return False
    
        if not self.tower_manager():
            print("You can't place a tower here")
            return False
        self.gold -= tw.Tower.tower_types[tower][-1]

        return True