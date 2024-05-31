class Player:
    def __init__(self, name: str, gold: int, tower_manager: TowerManager):
        self.name = name
        self.gold = gold
        self.tower_manager = tower_manager
        self.placed_towers = []

    def can_afford_tower(self, tower: Tower) -> bool:
        return self.gold >= tower.cost

    def place_tower(self, tower: Tower, x: int, y: int) -> bool:
        if not self.can_afford_tower(tower):
            print(f"{self.name} cannot afford the {tower.name} tower.")
            return False
        if not self.tower_manager.place_tower(tower, x, y):
            print(f"Cannot place {tower.name} at position ({x}, {y}).")
            return False
        self.gold -= tower.cost
        self.placed_towers.append(tower)
        print(f"{self.name} placed a {tower.name} tower at ({x}, {y}).")
        return True