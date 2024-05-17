
import pygame
import pygame.gfxdraw

class UI():

    def __init__(self,
                 available_towers_graphics: list[pygame.Surface],
                 towers_coordinates: list[tuple[pygame.math.Vector2, pygame.math.Vector2]]) -> None:
        
        self.available_towers = available_towers_graphics
        self.towers_coordinates = towers_coordinates


    def draw(self, screen : pygame.Surface) -> None:
        pygame.gfxdraw.filled_circle(screen, 
                                     self.towers_coordinates[0][0] + 80,
                                     self.towers_coordinates[0][1] + 120,
                                     150,
                                     (0, 0, 255, 100))
        for tower, spot in zip(self.available_towers, self.towers_coordinates):
            screen.blit(tower, spot)