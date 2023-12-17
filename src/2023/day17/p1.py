import re
import numpy as np
from collections import deque
from collections import defaultdict
import itertools
import heapq

with open("example") as file:
    data: list = [line.removesuffix("\n") for line in file]

grid: list[list] = [list(line) for line in data]

def get_neighbor_coordinates(grid, zeile: int, spalte: int) -> list[tuple[int, int]]:
    """Get all cross neighbor coordinates in a 2D Grid"""
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (1, 0), (0, 1)]:
        nm, nn = zeile + dx, spalte + dy
        if 0 <= nm < len(grid[0]) and 0 <= nn < len(grid):
            neighbors.append((nm, nn))
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



heat_lost = 0
position = (0, 0)
def heuristic(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def a_star(grid, start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from: dict[tuple[int, int], None] = {start: None}
    cost_so_far: dict[tuple[int, int], int] = {start: 0}
    directions: dict[tuple[int, int], list[tuple[int, int]]] = {start: []}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        for next in get_neighbor_coordinates(grid, current[0], current[1]):
            # ↓(1, 0) ←(0, -1) ↑(-1, 0) →(0, 1)
            new_direction = (next[0] - current[0], next[1] - current[1])
            new_directions = directions[current] + [new_direction]

            # no more than 3 steps in one direction
            if len(new_directions) >= 3 and all(d == new_direction for d in new_directions[-3:]):
                continue
            # no 180° turns
            if len(new_directions) >= 1 and sum(new_directions[-1]) + sum(new_direction) == 0:
                continue

            new_cost = cost_so_far[current] + int(grid[next[0]][next[1]])
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current
                directions[next] = new_directions

    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


def display_grid(grid) -> None:
    """Display a 2D Grid"""
    print("\nGrid:")
    for line in grid:
        for e in line:
            print(e, end="")
        print("")

def display_path_in_grid(grid, path) -> None:
    """Display a 2D Grid"""
    print("\nGrid:")
    for m in range(len(grid)):
        for n in range(len(grid[0])):
            if (m, n) in path:
                print("·", end="")
            else:
                print(' ', end="")
        print("")



start, goal = (0, 0), (len(grid)-1, len(grid[0])-1)
print(f"Start: {start}, Goal: {goal}")
came_from, cost_so_far = a_star(grid, start, goal)
path = reconstruct_path(came_from, start, goal)

display_path_in_grid(grid, path)
