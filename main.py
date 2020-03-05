import numpy
import noise
import random
import pygame
import sys
from time import sleep
import datetime


class Map:
    def __init__(self, seed=None, cutoff_percentage=50):
        self.cutoff_percentage = cutoff_percentage
        self.grids = [numpy.empty((grid_width, grid_height), float)]
        self.current_grid = self.grids[0]
        self.seed = seed if seed else hash(str(datetime.datetime.now()))
        self.regenerate()

    def generate_initial_grid(self):
        random.seed(self.seed)
        for y in range(grid_height):
            for x in range(grid_width):
                self.current_grid[x, y] = 0 if random.uniform(0, 100) < self.cutoff_percentage else 1

    def smooth_map(self, factor=1):
        for iteration in range(factor):
            for x in range(grid_width):
                for y in range(grid_height):
                    surrounding_count = len(self.get_surrounding(x, y))
                    if surrounding_count > 4:
                        self.current_grid[x, y] = 1
                    elif surrounding_count < 4:
                        self.current_grid[x, y] = 0
                    self.display(False, x, y)

    def connect_rooms(self, passage_size=5):
        pass

    def display(self, full=True, x=0, y=0):
        if full:
            for x in range(grid_width):
                for y in range(grid_height):
                    color = self.current_grid[x, y] * 255
                    pygame.draw.rect(screen, [color, color, color],
                                     (tile_width * x, tile_height * y, tile_width, tile_height))
                    # pygame.display.update((tile_width * x, tile_height * y, tile_width, tile_height))
        else:
            color = [self.current_grid[x, y] * 255] * 3
            pygame.draw.rect(screen, color,
                             (tile_width * x, tile_height * y, tile_width, tile_height))
            pygame.display.update((tile_width * x, tile_height * y, tile_width, tile_height))

    def regenerate(self, seed=None):
        self.seed = seed if seed else hash(str(datetime.datetime.now()))
        self.generate_initial_grid()
        self.display()

    def get_surrounding(self, x, y, distance=1, wall=True, space=False):
        surrounding_coordinates = [
            (x, y - distance),
            (x + distance, y),
            (x, y + distance),
            (x - distance, y),
            (x - distance, y - distance),
            (x + distance, y + distance),
            (x - distance, y + distance),
            (x + distance, y - distance)
        ]

        return [self.current_grid[surrounding_coordinate] for surrounding_coordinate in surrounding_coordinates
                if not self.is_out_of_bounds(surrounding_coordinate)
                and ((wall and self.current_grid[surrounding_coordinate] == 1)
                     or (space and self.current_grid[surrounding_coordinate] == 0))]

    @staticmethod
    def is_out_of_bounds(coordinates):
        x, y = coordinates
        return not (0 <= x < grid_width and 0 <= y < grid_height)

    class Grid:
        def __init__(self, seed=None, cutoff_percentage=50):
            self.cutoff_percentage = cutoff_percentage
            self.grid = numpy.empty((grid_width, grid_height), float)
            self.seed = seed if seed else hash(str(datetime.datetime.now()))


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
main = Map(cutoff_percentage=50)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F5:
                main.regenerate()
            if event.key == pygame.K_s:
                main.smooth_map()
            if event.key == pygame.K_c:
                main.connect_rooms()
    pygame.display.flip()
