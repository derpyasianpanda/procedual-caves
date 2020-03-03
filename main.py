import numpy
import noise
import random
import pygame
import sys


class Map:
    def __init__(self, seed=None):
        self.map_grid = numpy.empty((grid_width, grid_height), float)
        random.seed(seed)
        self.seed = int(random.random() * 1000)
        self.generate_map()

    def generate_map(self):
        for x in range(grid_width):
            for y in range(grid_height):
                self.map_grid[x, y] = noise.pnoise2(x / grid_width, y / grid_height,
                                                    persistence=5, octaves=3, base=self.seed)
        self.smooth_map()
        self.connect_rooms()

    def smooth_map(self, factor=1):
        pass

    def connect_rooms(self, passage_size=5):
        pass

    def display(self):
        for x in range(grid_width):
            for y in range(grid_height):
                color = int(((self.map_grid[x, y] / 2) + .5) * 255)
                pygame.draw.rect(screen, [color, color, color],
                                 (tile_width * x, tile_height * y, tile_width, tile_height))


grid_width = 300
grid_height = 300
display_width = 600
display_height = 600
tile_width = display_width // grid_width
tile_height = display_height // grid_height

pygame.init()
screen = pygame.display.set_mode((display_width, display_height))
screen.fill([255, 255, 255])
main = Map()
main.display()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
