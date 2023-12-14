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


#gridc = copy.deepcopy(grid)

for m in range(len(grid)):
    for n in range(len(grid[0])):
        if grid[m][n] == 'O':
            _m, _n = move_up(grid, m, n)
            print(f"{_m}, {n} -> {m}, {n}")
            if m != _m:
                grid[_m][_n] = 'O'
                grid[m][n] = '.'


print(grid[0])

rock_load = 0
for m in range(len(grid)):
    for n in range(len(grid[0])):
        if grid[m][n] == 'O':
            rock_load += len(grid) - m

display_pattern(grid)
print(rock_load)