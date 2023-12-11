import itertools

with open("input") as file:
    data: list = [line.removesuffix("\n") for line in file]

grid: list[list] = [list(line) for line in data]

def manhattan_distance(x1, y1, x2, y2):
    """Manhattan Distance between two points (x1, y1) and (x2, y2)"""
    return abs(x1 - x2) + abs(y1 - y2)

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
    print("empty_rows", empty_rows)
    print("empty_cols", empty_cols)
    for row in sorted(empty_rows, reverse=True):
        grid.insert(row, ["." for _ in grid[0]])

    for col in sorted(empty_cols, reverse=True):
        for row in grid:
            row.insert(col, ".")

    return grid

expanded_grid = expand_universe(grid)

numbered_grid, galaxy_positions = number_galaxies(expanded_grid.copy())

print(galaxy_positions)

distances = 0
galaxy_pairs = itertools.combinations(galaxy_positions.keys(), 2)

for g in galaxy_pairs:
    x_a, y_a = galaxy_positions[g[0]]
    x_b, y_b = galaxy_positions[g[1]]
    distances += manhattan_distance(x_a, y_a, x_b, y_b)
    print(f"Distance from {g[0]} to {g[1]} is {manhattan_distance(x_a, y_a, x_b, y_b)}")

print(f"Total distance is {distances}")


#for l in expanded_grid:
#    for i in l:
#        print(i, end="")
#    print()