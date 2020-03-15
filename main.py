import numpy
import random
import pygame
import sys
from time import sleep
import datetime
import copy


class GridCollection:
    def __init__(self, cutoff_percentage=50):
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
                pygame.draw.rect(screen, grid[x, y].color,
                                 (tile_width * x, tile_height * y, tile_width, tile_height))
                if not fast:
                    pygame.display.update((tile_width * x, tile_height * y, tile_width, tile_height))


class Grid:
    def __init__(self, seed, cutoff_percentage):
        self.cutoff_percentage = cutoff_percentage
        self.grid = numpy.empty((grid_width, grid_height), Tile)
        self.seed = seed
        self.generate_initial_grid()
        self.room_regions = self.generate_regions(0)
        self.wall_regions = self.generate_regions(1)

    def generate_initial_grid(self):
        random.seed(self.seed)
        for y in range(grid_height):
            for x in range(grid_width):
                self.grid[x, y] = Tile(x, y, tile_type=0) if random.uniform(0, 100) < self.cutoff_percentage \
                    else Tile(x, y, tile_type=1)

    def smooth_map(self, factor=1):
        for iteration in range(factor):
            for x in range(grid_width):
                for y in range(grid_height):
                    surrounding_count = len(self.get_surrounding(x, y))
                    if surrounding_count > 4:
                        self.grid[x, y].tile_type = 1
                    elif surrounding_count < 4:
                        self.grid[x, y].tile_type = 0

        self.room_regions = self.generate_regions(0)
        self.wall_regions = self.generate_regions(1)
        print(len(self.room_regions), len(self.wall_regions))

    def generate_regions(self, tile_type):
        checked = numpy.full((grid_width, grid_height), False)
        regions = []
        for x in range(grid_width):
            for y in range(grid_height):
                if not checked[x, y] and self.grid[x, y].tile_type == tile_type:
                    region = self.get_region_tiles(self.grid[x, y])
                    regions.append(region)
                    for tile in region:
                        checked[tile.coordinate] = True
        return regions

    def get_region_tiles(self, tile):
        tiles = []
        checked = numpy.full((grid_width, grid_height), False)
        tile_type = tile.tile_type

        to_check = [tile]
        checked[tile.coordinate] = True
        while to_check:
            current_tile = to_check.pop()
            tiles.append(current_tile)
            for next_tile in self.get_surrounding(tile=current_tile, diagonals=False, tile_types=[tile_type]):
                if not checked[next_tile.coordinate]:
                    checked[next_tile.coordinate] = True
                    to_check.append(next_tile)
        return tiles

    def connect_rooms(self, passage_size=5):
        pass

    def get_surrounding(self, x=0, y=0, tile=None, distance=1, diagonals=True, tile_types=[1], coordinate=False):
        if tile:
            x, y = tile.coordinate

        adjacent_coordinates = [
            (x, y - distance),
            (x + distance, y),
            (x, y + distance),
            (x - distance, y)
        ]

        result = [(self.grid[adjacent_coordinate] if not coordinate else adjacent_coordinate)
                  for adjacent_coordinate in adjacent_coordinates
                  if not self.is_out_of_bounds(adjacent_coordinate)
                  and self.grid[adjacent_coordinate].tile_type in tile_types]

        if not diagonals:
            return result

        diagonal_coordinates = [
            (x - distance, y - distance),
            (x + distance, y + distance),
            (x - distance, y + distance),
            (x + distance, y - distance)
        ]

        result += [(self.grid[diagonal_coordinate] if not coordinate else diagonal_coordinate)
                   for diagonal_coordinate in diagonal_coordinates
                   if not self.is_out_of_bounds(diagonal_coordinate)
                   and self.grid[diagonal_coordinate].tile_type in tile_types]

        return result

    @staticmethod
    def is_out_of_bounds(coordinates):
        x, y = coordinates
        return not (0 <= x < grid_width and 0 <= y < grid_height)


class Tile:
    def __init__(self, x=0, y=0, coordinate=None, tile_type=0, debug=False):
        if coordinate:
            self.x, self.y = coordinate
            self.coordinate = coordinate
        else:
            self.x, self.y = x, y
            self.coordinate = (x, y)

        self.tile_type = tile_type
        self.debug = False

    @property
    def color(self):
        if self.debug:
            return [0, 0, 255] if bool(self.tile_type) else [255, 0, 0]
        else:
            return [self.tile_type * 255] * 3


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
main = GridCollection(cutoff_percentage=50)

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
