import re
import numpy as np
from collections import deque
from collections import defaultdict
import itertools

from shapely import Point
from shapely.geometry import Polygon
from shapely.ops import transform
from shapely.ops import cascaded_union
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

def display_lagoon(polygon) -> None:
    p = gpd.GeoSeries(polygon)
    p.plot()
    #plt.show()
    plt.savefig("part2.2.png")

digging_plan: list[tuple[int, int]] = []
start = (0, 0)
for l in data:
    # Path 1
    direction = l.split(" ")[0]
    length = int(l.split(" ")[1])

    # Path 2
    color = l.split(" ")[2][2:-1]
    if color[-1] == '0':
        direction = 'R'
    elif color[-1] == '1':
        direction = 'D'
    elif color[-1] == '2':
        direction = 'L'
    elif color[-1] == '3':
        direction = 'U'
    length = int(color[0:-1], base=16)

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

polygon_a = Polygon(digging_plan)
polygon_b = transform(lambda x, y: (x + 1, y), polygon_a)
polygon_c = transform(lambda x, y: (x, y + 1), polygon_a)
polygon_d = transform(lambda x, y: (x + 1, y + 1), polygon_a)

polygons = [polygon_a, polygon_b, polygon_c, polygon_d]

display_lagoon(polygons)

u = cascaded_union(polygons)
print("93325932219961 to high")
print(u.area)

# Use the function
#grid = count_points(Polygon(digging_plan))
#print(grid)
