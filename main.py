import numpy
import noise
import random
import pygame
import sys
from time import sleep
import datetime


class Map:
    def __init__(self, seed=None):
        self.map_grid = numpy.empty((grid_width, grid_height), float)
        self.seed = seed if seed else hash(str(datetime.datetime.now()))
        self.regenerate()

    def generate_map(self):
        print(self.seed)
        random.seed(self.seed)
        temp = random.choices([0, 1], k=grid_width * grid_height)
        for y in range(grid_height):
            for x in range(grid_width):
                self.map_grid[x, y] = temp[10 * y + x]
        self.smooth_map()
        self.connect_rooms()

    def smooth_map(self, factor=1):
        pass

    def connect_rooms(self, passage_size=5):
        pass

    def display(self):
        for x in range(grid_width):
            for y in range(grid_height):
                color = self.map_grid[x, y] * 255
                pygame.draw.rect(screen, [color, color, color],
                                 (tile_width * x, tile_height * y, tile_width, tile_height))
                # pygame.display.update((tile_width * x, tile_height * y, tile_width, tile_height))

    def regenerate(self, seed=None):
        if self.seed:
            random.seed(self.seed)
        self.seed = seed if seed else hash(str(datetime.datetime.now()))
        self.generate_map()
        self.display()


grid_width = 250
grid_height = 150
display_width = 1000
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
    pygame.display.flip()
