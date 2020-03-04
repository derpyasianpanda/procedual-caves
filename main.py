import numpy
import noise
import random
import pygame
import sys
from time import sleep
import datetime


class Map:
    def __init__(self, seed=None):
        self.initial_grid = numpy.empty((grid_width, grid_height), float)
        self.second_grid = None  # Smoothed grid
        self.final_grid = None  # Connected grid
        self.seed = seed if seed else hash(str(datetime.datetime.now()))
        self.regenerate()

    def generate_initial_grid(self):
        random.seed(self.seed)
        for y in range(grid_height):
            for x in range(grid_width):
                self.initial_grid[x, y] = random.randint(0, 1)

    def smooth_map(self, factor=1):
        pass

    def connect_rooms(self, passage_size=5):
        pass

    def display(self):
        for x in range(grid_width):
            for y in range(grid_height):
                color = self.initial_grid[x, y] * 255
                pygame.draw.rect(screen, [color, color, color],
                                 (tile_width * x, tile_height * y, tile_width, tile_height))
                # pygame.display.update((tile_width * x, tile_height * y, tile_width, tile_height))

    def regenerate(self, seed=None):
        self.seed = seed if seed else hash(str(datetime.datetime.now()))
        self.generate_initial_grid()
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
