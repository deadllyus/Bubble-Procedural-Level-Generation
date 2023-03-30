# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 12:15:29 2023

@author: Onur
"""
import random


class CellGroup:
    def __init__(self, color):
        self.color = color
        self.cells = []
        self.length = 0

    def add_cell(self, cell):
        self.cells.append(cell)

    def get_length(self):
        return len(self.cells)

    def __repr__(self):
        return "color: " + str(self.color) + " cells: " + str(self.cells)


class HexCell:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.is_connected_to_center = False
        self.group = CellGroup(self.color)
        self.group.add_cell(self)

    def get_distance(self, cell1, cell2):
        return abs(cell2.x - cell1.x) + abs(cell2.y - cell1.y)

    def get_right(self, grid):
        right = grid[self.y][self.x + 1]
        return right

    def get_left(self, grid):
        left = grid[self.y][self.x - 1]
        return left

    def get_top_right(self, grid):
        if self.y % 2 != 0:
            top_right = grid[self.y - 1][self.x + 1]
        else:
            top_right = grid[self.y - 1][self.x]
        return top_right

    def get_top_left(self, grid):
        if self.y % 2 != 0:
            top_left = grid[self.y - 1][self.x]
        else:
            top_left = grid[self.y - 1][self.x - 1]
        return top_left

    def get_bottom_left(self, grid):
        if self.y % 2 != 0:
            bottom_left = grid[self.y + 1][self.x]
        else:
            bottom_left = grid[self.y + 1][self.x - 1]
        return bottom_left

    def get_bottom_right(self, grid):
        if self.y % 2 != 0:
            bottom_right = grid[self.y + 1][self.x + 1]
        else:
            bottom_right = grid[self.y + 1][self.x]
        return bottom_right

    def get_neighbors(self, grid):
        return [self.get_right(grid), self.get_top_right(grid), self.get_top_left(grid),
                self.get_left(grid), self.get_bottom_left(grid), self.get_bottom_right(grid)]

    def get_empty_cell(self, grid):
        neighbors = self.get_neighbors(grid)
        empty_neighbors = []
        for i in range(len(neighbors)):
            cell = neighbors[i]
            if cell.color == 0:
                empty_neighbors.append(cell)

        if len(empty_neighbors) <= 0:
            return random.choice(neighbors).get_empty_cell(grid)

        return random.choice(empty_neighbors)


    def get_random_empty_neighbor(self, grid):
        neighbors = self.get_neighbors(grid)
        empty_neighbors = []
        same_color_neighbors = []

        for i in range(len(neighbors)):
            cell = neighbors[i]
            if cell.color == 0 and not cell.is_connected_to_center:
                empty_neighbors.append(cell)
            if cell.color == self.color:
                same_color_neighbors.append(cell)

        if len(empty_neighbors) <= 0:
            if len(same_color_neighbors) > 0:
                try:
                    return random.choice(same_color_neighbors).get_random_empty_neighbor(grid)
                except:
                    # print("max recursion depth")
                    return None
            else:
                #print("no empty neighbors or no same color neighbor with empty neighbors")
                pass

            return None

        return random.choice(empty_neighbors)

    def spread(self, grid):
        new_cell = self.get_random_empty_neighbor(grid)
        new_cell.color = self.color
        new_cell.group = self.group
        self.group.add_cell(new_cell)
        return new_cell

    def __repr__(self):
        return "x: " + str(self.x) + " y: " + str(self.y) + " color: " + str(self.color)
