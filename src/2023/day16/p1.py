import sys

import numpy as np

with open("input") as file:
    data: list = [line.removesuffix("\n") for line in file]

def display_grid(grid) -> None:
    """Display a 2D Grid"""
    print("\nGrid:")
    for line in grid:
        for e in line:
            print(e, end="")
        print("")


sys.setrecursionlimit(10000)

grid: list[list] = [list(line) for line in data]

def energize(position, direction):
    global egrid, visited
    while 0 <= position[0] < len(grid) and 0 <= position[1] < len(grid[0]):
        if egrid[position[0]][position[1]] > 0 and visited[position[0]][position[1]] == direction:
            return
        egrid[position[0]][position[1]] += 1
        visited[position[0]][position[1]] = direction

        e = grid[position[0]][position[1]]
        if e == '.' or (direction[0] == 0 and e == '-') or (direction[1] == 0 and e == '|'):
            position = (position[0] + direction[0], position[1] + direction[1])
        elif e == '/':
            direction = (-direction[1], -direction[0])
            position = (position[0] + direction[0], position[1] + direction[1])
        elif e == '\\':
            direction = (direction[1], direction[0])
            position = (position[0] + direction[0], position[1] + direction[1])
        elif e == '|' and direction[0] == 0:
            energize((position[0] + 1, position[1]), (1, 0))
            position = (position[0] - 1, position[1])
            direction = (-1, 0)
        elif e == '-' and direction[1] == 0:
            energize((position[0], position[1] + 1), (0, 1))
            position = (position[0], position[1] - 1)
            direction = (0, -1)


direction = (0, 1)
position = (0, 0)

egrid = np.zeros((len(grid), len(grid[0])), dtype=int)
visited: list[list[tuple]] = egrid.copy().tolist()

def energized_fields(position, direction) -> int:
    global egrid, visited
    egrid = np.zeros((len(grid), len(grid[0])), dtype=int)
    visited = egrid.copy().tolist()
    energize(position, direction)
    #display_grid(visited)
    return np.sum(egrid != 0)

energized_fields((0, 0), (0, 1))

energetization: list[int] = []
for m in range(len(grid)):
    # →
    energetization.append(energized_fields((m, 0), (0, 1)))
    # ←
    energetization.append(energized_fields((m, len(grid[0])-1), (0, -1)))
    print(m)

for n in range(len(grid[0])):
    # ↓
    energetization.append(energized_fields((0, n), (1, 0)))
    # ↑
    energetization.append(energized_fields((len(grid)-1, n), (-1, 0)))
    print(n)

print(f"Maximal energization: {max(energetization)}")