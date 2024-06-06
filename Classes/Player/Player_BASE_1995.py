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
            if tw.tower_types[tower][-1] <= self.gold:
               affordable.append(tower) 
        return affordable

    def place_tower(self, tower: tw.Tower, x: int, y: int, ) -> bool:
        if not self.can_afford_tower(tower):
            print(f"{self.name} cannot afford the {tower.name} tower.")
            return False
    
        if not self.tower_manager():
            print(f"Cannot place {tower.name} at position ({x}, {y}).")
            return False
        self.gold -= tower.cost

        print(f"{self.name} placed a {tower.name} tower at ({x}, {y}).")
        return True