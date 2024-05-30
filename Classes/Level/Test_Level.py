from typing import List, Dict, Tuple

class Level:
    def __init__(self, level_number: int):
        self.level_number = level_number
        self.enemy_waves: List[Dict[str, Tuple[int, int]]] = []

    def add_wave(self, enemy_type: Enemy, quantity: int, interval: int):
        self.enemy_waves.append({"enemy": enemy_type, "quantity": quantity, "interval": interval})

    def get_waves(self) -> List[Dict[str, Tuple[int, int]]]:
        return self.enemy_waves

    def start_level(self):
        for wave in self.enemy_waves:
            enemy = wave["enemy"]
            quantity = wave["quantity"]
            interval = wave["interval"]
            print(f"Spawning {quantity} {enemy.name}(s) every {interval} seconds.")

# Use example:
if __name__ == "__main__":

    level1 = Level(level_number=1)
    level1.add_wave(enemy_type=student, quantity=10, interval=5)
    level1.start_level()

