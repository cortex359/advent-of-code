import itertools

with open("input") as file:
    data: list = [line.removesuffix("\n") for line in file]

grid: list[list] = [list(line) for line in data]

def manhattan_distance(x1, y1, x2, y2):
    """Manhattan Distance between two points (x1, y1) and (x2, y2)"""
    return abs(x1 - x2) + abs(y1 - y2)

def show_grid(grid):
    for l in grid:
        for i in l:
            print(i, end="")
        print()

def number_galaxies(grid):
    galaxy_number = 1
    galaxy_positions = {}

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '#':
                grid[i][j] = str(galaxy_number)
                galaxy_positions[galaxy_number] = (i, j)
                galaxy_number += 1

    return grid, galaxy_positions

def expand_universe(grid):
    empty_rows = [i for i in range(len(grid)) if not any(cell == '#' for cell in grid[i])]
    empty_cols = [j for j in range(len(grid[0])) if not any(grid[i][j] == '#' for i in range(len(grid)))]
    return empty_rows, empty_cols

empty_rows, empty_cols = expand_universe(grid.copy())

numbered_grid, galaxy_positions = number_galaxies(grid.copy())

print(galaxy_positions)

distances = 0
galaxy_pairs = itertools.combinations(galaxy_positions.keys(), 2)

def crossing_expanded_regions(empty_rows, empty_cols, pos_a, pos_b):
    crossings = 0
    for c in empty_rows:
        if pos_a[0] <= c <= pos_b[0] or pos_b[0] <= c <= pos_a[0]:
            crossings += 1
    for c in empty_cols:
        if pos_a[1] <= c <= pos_b[1] or pos_b[1] <= c <= pos_a[1]:
            crossings += 1
    return crossings

for g in galaxy_pairs:
    x_a, y_a = galaxy_positions[g[0]]
    x_b, y_b = galaxy_positions[g[1]]
    normal_distance = manhattan_distance(x_a, y_a, x_b, y_b)
    crossings = crossing_expanded_regions(empty_rows, empty_cols, galaxy_positions[g[0]], galaxy_positions[g[1]])
    print(f"Normal distance from {g[0]} to {g[1]} is {manhattan_distance(x_a, y_a, x_b, y_b)} + {crossings} crossings")
    print(f"Adding {normal_distance + crossings}")
    distances += normal_distance + crossings * (1000000 - 1)

# 702770569197
print(f"Total distance is {distances}")