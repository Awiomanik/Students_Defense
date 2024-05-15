# prototipical map class

# IMPORTS
import pygame

class Map():
    def __init__(self,
                 graphic_path : str,
                 resolution : tuple[int, int],
                 ) -> None:
        # load image and scale it to screen size
        self.image = pygame.transform.scale(pygame.image.load(graphic_path), resolution)  
        # get enemies paths
        self.enemies_path, self.enemies_path_widths = self.load_enemies_paths(graphic_path.rsplit('.', 1)[0] + '.dat')


    def load_enemies_paths(self, path) -> tuple[list[tuple[int, int]], list[int]]:
        with open(path) as file:
            path_raw = file.readlines()

        path_raw = [line.strip().split(', ') for line in path_raw[2:]]  
        return [(int(line[0]), int(line[1])) for line in path_raw], [int(line[2]) for line in path_raw[:-1]]
    
    def draw(self, screen):
        screen.blit(self.image, (0, 0))