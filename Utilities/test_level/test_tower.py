"""Prototipical defense class"""

import pygame

vec = pygame.math.Vector2

class Defense():
    board: list[tuple[vec, vec]]  = []

    def __init__(self,
                 graphic_path: str,
                 placement: tuple[int, int],
                 size: tuple[int, int] = (150, 225),
                 power: int = 10) -> None:
        
        Defense.board.append((vec(placement), vec(tuple(map(sum, zip(placement, size))))))

        self.place = placement

        # Image loaded and scaled it to the given size
        self.face = pygame.transform.scale(pygame.image.load(graphic_path), size)

        self.power = power

    def occupied(self, spot: tuple[vec, vec]) -> bool:
        for (bottom_left, top_right) in Defense.board:
            # Check for overlap
            # Spot[0] is bottom-left and Spot[1] is top-right of the new rectangle
            if not (spot[1].x <= bottom_left.x or  # Spot's right edge is left of the bottom_left's x
                    spot[0].x >= top_right.x or   # Spot's left edge is right of the top_right's x
                    spot[1].y <= bottom_left.y or  # Spot's top edge is below the bottom_left's y
                    spot[0].y >= top_right.y):     # Spot's bottom edge is above the top_right's y
                return True  # There is an overlap
        return False  # No overlaps found
    
    def draw(self, screen : pygame.Surface) -> None:
        screen.blit(self.face, self.place)




