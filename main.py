import numpy
import random
import pygame
import sys
from time import sleep
import datetime
import copy


class Map:
    def __init__(self, seed=None, cutoff_percentage=50):
        self.cutoff_percentage = cutoff_percentage
        self.regenerate()

    def regenerate(self, seed=None):
        self.current_grid = 0
        self.seed = seed if seed else hash(str(datetime.datetime.now()))
        self.grids = [Grid(self.seed, self.cutoff_percentage)]
        self.display(self.grids[self.current_grid])

    def action(self, action):
        new_grid = copy.deepcopy(self.grids[self.current_grid])
        actions = {
            "smooth": new_grid.smooth_map,
            "connect": new_grid.connect_rooms
        }
        actions[action]()
        self.grids = self.grids[:self.current_grid + 1] + [new_grid]
        self.current_grid += 1
        self.display(self.grids[self.current_grid], False)

    def grid_change(self, change=-1):
        if self.current_grid + change not in [-1, len(self.grids)]:
            self.current_grid += change
            self.display(self.grids[self.current_grid])

    @staticmethod
    def display(grid, fast=True):
        grid = grid.grid
        for x in range(grid_width):
            for y in range(grid_height):
                color = [grid[x, y] * 255] * 3
                pygame.draw.rect(screen, color,
                                 (tile_width * x, tile_height * y, tile_width, tile_height))
                if not fast:
                    pygame.display.update((tile_width * x, tile_height * y, tile_width, tile_height))


class Grid:
    def __init__(self, seed, cutoff_percentage):
        self.cutoff_percentage = cutoff_percentage
        self.grid = numpy.empty((grid_width, grid_height), float)
        self.seed = seed
        self.generate_initial_grid()

    def generate_initial_grid(self):
        random.seed(self.seed)
        for y in range(grid_height):
            for x in range(grid_width):
                self.grid[x, y] = 0 if random.uniform(0, 100) < self.cutoff_percentage else 1

    def smooth_map(self, factor=1):
        for iteration in range(factor):
            for x in range(grid_width):
                for y in range(grid_height):
                    surrounding_count = len(self.get_surrounding(x, y))
                    if surrounding_count > 4:
                        self.grid[x, y] = 1
                    elif surrounding_count < 4:
                        self.grid[x, y] = 0

    def connect_rooms(self, passage_size=5):
        pass

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

        return [self.grid[surrounding_coordinate] for surrounding_coordinate in surrounding_coordinates
                if not self.is_out_of_bounds(surrounding_coordinate)
                and ((wall and self.grid[surrounding_coordinate] == 1)
                     or (space and self.grid[surrounding_coordinate] == 0))]

    @staticmethod
    def is_out_of_bounds(coordinates):
        x, y = coordinates
        return not (0 <= x < grid_width and 0 <= y < grid_height)


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
                main.action("smooth")
            if event.key == pygame.K_c:
                main.action("connect")
            if event.key == pygame.K_LEFT:
                main.grid_change(-1)
            if event.key == pygame.K_RIGHT:
                main.grid_change(1)
    pygame.display.flip()
