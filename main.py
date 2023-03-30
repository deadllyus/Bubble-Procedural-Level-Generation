# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 12:36:30 2023

@author: Onur
"""
from Hexagonal import HexCell
import random
import time


def extract_data(input_string):
    start_tag = '<data encoding="csv">'
    end_tag = '</data>'
    start_index = input_string.find(start_tag) + len(start_tag)
    end_index = input_string.find(end_tag, start_index)
    if start_index == -1 or end_index == -1:
        return ""
    else:
        return input_string[start_index:end_index].strip()


def data_to_matrix(data):
    data = data.split("\n")
    for i in range(len(data)):
        data[i] = data[i].split(",")
        if data[i][-1] == "":
            del data[i][-1]
    for i in range(len(data)):
        for j in range(len(data[0])):
            data[j][i] = eval(data[j][i])

    return data


def generate_grid(group_size):
    f = open("test_tiled.tmx", "r")
    data = f.read()
    f.close()

    data = extract_data(data)

    grid = data_to_matrix(data)

    center = ()  # most of the time this is (40,46)
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 1:
                center = (x, y)
                break

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if x == center[0] and y == center[1]:
                grid[y][x] = HexCell(x, y, 1)
                grid[y][x].is_connected_to_center = True
            else:
                grid[y][x] = HexCell(x, y, 0)

    center_cell = grid[46][40]
    center_cell.is_connected_to_center = True

    color_list = [2, 3, 4, 6]
    prev_color = -1
    for i in range(group_size):
        curr_cell = center_cell.get_empty_cell(grid)
        dummy_color_list = color_list.copy()
        for neighbor in curr_cell.get_neighbors(grid):
            if neighbor.color in dummy_color_list:
                dummy_color_list.remove(neighbor.color)
        curr_cell.color = random.choice(dummy_color_list)
        while curr_cell.group.get_length() < 9:
            curr_cell = curr_cell.spread(grid)




    return grid


def save_grid(grid):
    output_grid = [[0 for i in range(100)] for j in range(100)]

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            output_grid[y][x] = grid[y][x].color

    filename = 'my_array.tmx'
    start = '<?xml version="1.0" encoding="UTF-8"?>\n<map version="1.5" tiledversion="1.7.2" orientation="hexagonal" renderorder="right-down" width="100" height="100" tilewidth="100" tileheight="170" infinite="0" hexsidelength="0" staggeraxis="y" staggerindex="odd" nextlayerid="2" nextobjectid="1">\n <tileset firstgid="1" source="D:/GBot Games/bubble/Assets/Maps/Maps Onur/bubbles.tsx"/>\n <layer id="1" name="Tile Layer 1" width="100" height="100">\n  <data encoding="csv">'
    end = '\n</data>\n </layer>\n</map>'
    res_string = ""

    # Loop over each row in the array
    for row in output_grid:
        # Write each element in the row, separated by commas
        res_string += ','.join(str(x) for x in row) + ',\n'

    res_string = res_string[0:-2:1]
    res_string = start + res_string + end

    f = open(filename, "w")
    f.write(res_string)
    f.close()

def main():
    i = 0

    while i < 26:
        for j in range(100):
            try:
                grid = generate_grid(i)
                save_grid(grid)
                print("Group size: " + str(i))
                i += 1
                time.sleep(0.5)
            except:
                pass

if __name__ == "__main__":
    main()
