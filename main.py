import numpy
import noise
import random
import pygame
import sys
from time import sleep


class Map:
    def __init__(self, seed=None):
        self.map_grid = numpy.empty((grid_width, grid_height), float)
        self.seed = seed
        self.base_seed = int(random.random() * 1000)
        self.display_mode = self.display_map
        self.regenerate()

    def generate_map(self):
        for x in range(grid_width):
            for y in range(grid_height):
                self.map_grid[x, y] = noise.snoise2(x / grid_width, y / grid_height,
                                                    persistence=1, octaves=2, base=self.base_seed)
        self.smooth_map()
        self.connect_rooms()

    def smooth_map(self, factor=1):
        pass

    def connect_rooms(self, passage_size=5):
        pass

    def change_display_mode(self):
        self.display_mode = self.display_cave if self.display_mode == self.display_map else self.display_map
        self.display_mode()

    def display_map(self):
        for x in range(grid_width):
            for y in range(grid_height):
                color = int(((self.map_grid[x, y] / 2) + .5) * 255)
                pygame.draw.rect(screen, [color, color, color],
                                 (tile_width * x, tile_height * y, tile_width, tile_height))
                pygame.display.update((tile_width * x, tile_height * y, tile_width, tile_height))

    def display_cave(self):
        for x in range(grid_width):
            for y in range(grid_height):
                pygame.draw.rect(screen, [0, 0, 0] if self.map_grid[x, y] < 0 else [255, 255, 255],
                                 (tile_width * x, tile_height * y, tile_width, tile_height))
                pygame.display.update((tile_width * x, tile_height * y, tile_width, tile_height))

    def regenerate(self, seed=None):
        if self.seed:
            random.seed(self.seed)
        self.base_seed = int(random.random() * 1000)
        self.generate_map()
        self.display_mode()


grid_width = 25
grid_height = 25
display_width = 600
display_height = 600
tile_width = display_width // grid_width
tile_height = display_height // grid_height
step_time = 0

pygame.init()
screen = pygame.display.set_mode((display_width, display_height))
screen.fill([255, 255, 255])
main = Map()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F5:
                main.regenerate()
            if event.key == pygame.K_SPACE:
                main.change_display_mode()
    pygame.display.flip()
