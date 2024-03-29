import re
import numpy as np
from collections import deque
from collections import defaultdict
import itertools

from shapely import Point
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import geopandas as gpd


with open("input") as file:
    data: list = [line.removesuffix("\n") for line in file]

grid: list[list] = [list(line) for line in data]


def display_grid(grid) -> None:
    """Display a 2D Grid"""
    print("\nGrid:")
    for line in grid:
        for e in line:
            if e == 0:
                print(".", end="")
            elif e == 1:
                print("#", end="")
        print("")

def display_lagoon(edges) -> None:
    p = gpd.GeoSeries(Polygon(edges))
    p.plot()
    plt.show()
    plt.savefig("part1.png")
    #print(f"Area: {p.area}, Length: {p.length}")


digging_plan: list[tuple[int, int]] = []
start = (0, 0)
for l in data:
    direction = l.split(" ")[0]
    length = int(l.split(" ")[1])
    color = l.split(" ")[2][2:-2]

    if direction == 'U':
        end = (start[0], start[1] + length)
    elif direction == 'D':
        end = (start[0], start[1] - length)
    elif direction == 'L':
        end = (start[0] - length, start[1])
    elif direction == 'R':
        end = (start[0] + length, start[1])

    digging_plan.append(end)
    start = end

display_lagoon(digging_plan)

def count_points(polygon) -> int:
    # Get the bounds of the polygon
    minx, miny, maxx, maxy = polygon.bounds

    count = 0

    # Iterate over each cell in the grid
    for x in range(int(minx), int(maxx) + 1):
        for y in range(int(miny), int(maxy) + 1):
            point = Point(x, y)
            if polygon.contains(point) or polygon.touches(point):
                count += 1

    return count

# Use the function
grid = count_points(Polygon(digging_plan))
print(grid)
