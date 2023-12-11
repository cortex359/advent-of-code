import os
import re
import sys

import numpy as np
from collections import deque
from collections import defaultdict
import itertools
import copy

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()

input_file = sys.argv[1] if len(sys.argv) > 1 else "input"
if not os.path.isfile(input_file):
    print(f"{Fore.RED}Input file {Style.BRIGHT}{input_file}{Style.NORMAL} not found!{Style.RESET_ALL}")
    exit(1)

with open(input_file) as file:
    data: list = [line.removesuffix("\n") for line in file]

grid: list[list] = [list(line) for line in data]

# 2D Grid Stuff
# -------------
def get_neighbor_coordinates(grid, zeile: int, spalte: int) -> list[tuple[int, int]]:
    """Get all cross neighbor coordinates in a 2D Grid"""
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = zeile + dx, spalte + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            neighbors.append((nx, ny))
    return neighbors


def get_neighbors(grid, zeile: int, spalte: int) -> list[tuple]:
    """Get all cross neighbor values in a 2D Grid"""
    neighbors = []
    for _x, _y in get_neighbor_coordinates(grid, zeile, spalte):
        neighbors.append(grid[_x][_y])
    return neighbors


def get_diagonal_coordinates(grid, zeile, spalte):
    """Get all diagonal neighbor coordinates in a 2D Grid"""
    neighbors = []
    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        nx, ny = zeile + dx, spalte + dy
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            neighbors.append((nx, ny))
    return neighbors


def get_diagonals(grid, zeile, spalte):
    """Get all diagonal neighbor values in a 2D Grid"""
    neighbors = []
    for _x, _y in get_diagonal_coordinates(grid, zeile, spalte):
        neighbors.append(grid[_x][_y])
    return neighbors


# Graph Stuff
# -----------
def create_graph(edges: list[tuple]) -> dict:
    """Create a Graph from a list of Edges"""
    graph: dict = {}
    for a, b in edges:
        if a not in graph:
            graph[a] = []
        if b not in graph:
            graph[b] = []
        graph[a].append(b)
        graph[b].append(a)  # Omit this for directed graphs
    return graph


def dfs(graph: dict, start, visited=None):
    """Depth-First Search (DFS)"""
    if visited is None:
        visited = set()
    visited.add(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited


def bfs(graph, start):
    """Breadth-First Search (BFS)"""
    visited, queue = set(), deque([start])
    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(set(graph[vertex]) - visited)
    return visited


def shortest_path(graph, start, end):
    """Shortest Path between two nodes in a Graph"""
    queue = deque([(start, [start])])
    visited = set()
    while queue:
        vertex, path = queue.popleft()
        if vertex == end:
            return path
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None


def has_cycle(graph, start):
    """Check if a Graph has a cycle"""
    visited, stack = set(), [(start, None)]
    while stack:
        node, parent = stack.pop()
        if node in visited:
            return True
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor != parent:
                stack.append((neighbor, node))
    return False


def manhattan_distance(x1, y1, x2, y2):
    """Manhattan Distance between two points (x1, y1) and (x2, y2)"""
    return abs(x1 - x2) + abs(y1 - y2)



# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# \ is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

# \|F
# |||
# J|L

# F-\
# L-J

start_position = (0, 0)
for m in range(len(grid)):
    for n in range(len(grid[m])):
        if grid[m][n] == 'S':
            start_position = (m, n)
        if grid[m][n] == '7':
            grid[m][n] = '\\'

grid_distances = copy.deepcopy(grid)

queue: deque[tuple[int, int, int]] = deque([(start_position[0], start_position[1], 0)])
while len(queue) > 0:
    entry = queue.popleft()
    m, n, distance = entry
    pos_pipe = grid[m][n]
    if type(grid_distances[m][n]) is int:
        grid_distances[m][n] = min(distance, grid_distances[m][n])
        continue

    for _m, _n in get_neighbor_coordinates(grid, m, n):
        neighbor = grid[_m][_n]
        if type(grid_distances[_m][_n]) is int:
            continue

        if (pos_pipe == '|' or pos_pipe == 'S') and _n == n:
            if _m == m - 1 and neighbor in ('|', 'F', '\\'):
                queue.append((_m, _n, distance + 1))
            elif _m == m + 1 and neighbor in ('|', 'J', 'L'):
                queue.append((_m, _n, distance + 1))
        if (pos_pipe == '-' or pos_pipe == 'S') and _m == m:
            if _n == n - 1 and neighbor in ('-', 'L', 'F'):
                queue.append((_m, _n, distance + 1))
            elif _n == n + 1 and neighbor in ('-', 'J', '\\'):
                queue.append((_m, _n, distance + 1))
        if pos_pipe == 'L':
            if _m == m - 1 and _n == n and neighbor in ('|', 'F', '\\'):
                queue.append((_m, _n, distance + 1))
            elif _m == m and _n == n + 1 and neighbor in ('-', 'J', '\\'):
                queue.append((_m, _n, distance + 1))
        if pos_pipe == 'J':
            if _m == m - 1 and _n == n and neighbor in ('|', 'F', '\\'):
                queue.append((_m, _n, distance + 1))
            elif _m == m and _n == n - 1 and neighbor in ('-', 'L', 'F'):
                queue.append((_m, _n, distance + 1))
        if pos_pipe == '\\':
            if _m == m + 1 and _n == n and neighbor in ('|', 'J', 'L'):
                queue.append((_m, _n, distance + 1))
            elif _m == m and _n == n - 1 and neighbor in ('-', 'L', 'F'):
                queue.append((_m, _n, distance + 1))
        if pos_pipe == 'F':
            if _m == m + 1 and _n == n and neighbor in ('|', 'J', 'L'):
                queue.append((_m, _n, distance + 1))
            elif _m == m and _n == n + 1 and neighbor in ('-', 'J', '\\'):
                queue.append((_m, _n, distance + 1))

    grid_distances[m][n] = distance


def raster(grid_distances):
    additions, last_additions = 1, 0
    while additions > last_additions:
        last_additions = additions
        for m in range(len(grid_distances)):
            for n in range(len(grid_distances[m])):
                if grid_distances[m][n] == '.':
                    neighbors = get_neighbors(grid_distances, m, n)
                    if len(neighbors) < 4 or 'ø' in neighbors:
                        grid_distances[m][n] = 'ø'
                        additions += 1



def raster_inside(grid_distances):
    for m in range(len(grid_distances)):
        for n in range(len(grid_distances[m])):
            if grid_distances[m][n] == '.':
                neighbors = get_neighbors(grid_distances, m, n)
                for ne in neighbors:
                    if type(ne) is int or ne.isdigit():
                        grid_distances[m][n] = 'I'


raster(grid_distances)
raster_inside(grid_distances)

counter = 0

def symbolize_pipes(s: str) -> str:
    return (s.replace('\\', '┐').replace('F', '┌')
            .replace('J', '┘').replace('L', '└')
            .replace('|', '│').replace('-', '─'))


def display_1(grid, grid_distances):
    counter: int = 0

    for m in range(len(grid_distances)):
        for n in range(len(grid_distances[m])):
            if type(grid_distances[m][n]) is int:
                e = symbolize_pipes(grid[m][n])
            else:
                e = grid_distances[m][n]
            if e == 'I':
                counter += 1
                e = f"{Fore.BLUE}I{Style.RESET_ALL}"
            else:
                e = f"{Style.DIM}{e}{Style.RESET_ALL}"
            print('{:1s}'.format(str(e)), end='')
        print()
    print(counter)


def display_2(grid, grid_distances):
    counter: int = 0
    for m in range(len(grid_distances)):
        for n in range(len(grid_distances[m])):
            if type(grid_distances[m][n]) is int:
                e = f"{grid_distances[m][n]:2d} "
            elif grid_distances[m][n] == 'I':
                counter += 1
                e = f"{Fore.BLUE} I {Style.RESET_ALL}"
            else:
                e = f"{grid_distances[m][n]:2s} "
                e = f"{Style.DIM}{e}{Style.RESET_ALL}"
            print('{:1s}'.format(str(e)), end='')
        print()
    print(counter)

display_1(grid, grid_distances)

