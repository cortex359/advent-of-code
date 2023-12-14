import copy
import re
import numpy as np
from collections import deque
from collections import defaultdict
import itertools

with open("input") as file:
    data: list = [line.removesuffix("\n") for line in file]

grid: list[list] = [list(line) for line in data]

def display_pattern(grid) -> None:
    """Display a 2D Grid"""
    print("\nPattern:")
    for line in grid:
        print("".join(line))


def move_up(grid, _m, n):
    while _m > 0 and grid[_m - 1][n] not in ('#', 'O'):
        _m = _m - 1
    return _m, n

def move_down(grid, _m, _n):
    while _m < len(grid) - 1 and grid[_m + 1][_n] not in ('#', 'O'):
        _m = _m + 1
    return _m, _n

def move_east(grid, _m, _n):
    while _n < len(grid[_m]) - 1 and grid[_m][_n + 1] not in ('#', 'O'):
        _n = _n + 1
    return _m, _n

def move_west(grid, _m, _n):
    while _n > 0 and grid[_m][_n - 1] not in ('#', 'O'):
        _n = _n - 1
    return _m, _n


def get_rock_load(grid):
    rock_load = 0
    for m in range(len(grid)):
        for n in range(len(grid[0])):
            if grid[m][n] == 'O':
                rock_load += len(grid) - m

    #display_pattern(grid)
    return rock_load


def do_cycle(grid):
    for move in (move_up, move_west):
        for m in range(len(grid)):
            for n in range(len(grid[0])):
                if grid[m][n] == 'O':
                    _m, _n = move(grid, m, n)
                    if m != _m or _n != n:
                        grid[_m][_n] = 'O'
                        grid[m][n] = '.'
        #get_rock_load(grid)

    for move in move_down, move_east:
        for m in range(len(grid)-1, -1, -1):
            for n in range(len(grid[0])-1, -1, -1):
                if grid[m][n] == 'O':
                    _m, _n = move(grid, m, n)
                    if m != _m or _n != n:
                        grid[_m][_n] = 'O'
                        grid[m][n] = '.'
        #get_rock_load(grid)

    return grid

state_list = []
pre_cycle_steps = 0

display_pattern(grid)

while str(grid) not in state_list:
    state_list.append(str(grid))
    grid = do_cycle(grid)
    #get_rock_load(grid)
    #display_pattern(grid)
    pre_cycle_steps += 1

print(f"Cycles to begin with {pre_cycle_steps}")

cycle_steps = 0
state_list_2 = []
rock_load_list = []
while str(grid) not in state_list_2:
    state_list_2.append(str(grid))
    grid = do_cycle(grid)
    rock_load_list.append(get_rock_load(grid))
    #display_pattern(grid)
    cycle_steps += 1

print(f"Steps afer one cyculation {cycle_steps}")

print(cycle_steps)
index = (1000000000 - pre_cycle_steps) % cycle_steps
print(f"index: {index}")
print(rock_load_list)
print(rock_load_list[index - 1])