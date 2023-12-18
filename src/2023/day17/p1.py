import re
import numpy as np
from collections import deque
from collections import defaultdict
import itertools
import heapq

with open("example") as file:
    data: list = [line.removesuffix("\n") for line in file]


def get_neighbor_coordinates(grid, zeile: int, spalte: int) -> list[tuple[int, int]]:
    """Get all cross neighbor coordinates in a 2D Grid"""
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nm, nn = zeile + dx, spalte + dy
        if 0 <= nm < len(grid) and 0 <= nn < len(grid[0]):
            neighbors.append((nm, nn))
    return neighbors


def manhattan_distance(a, b):
    """Manhattan Distance between two points (x1, y1) and (x2, y2)"""
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star(grid, start, goal):
    """
    Implementation of the A* search algorithm.

    Parameters:
    grid (list): A 2D list representing the grid.
    start (tuple): A tuple representing the starting coordinates.
    goal (tuple): A tuple representing the goal coordinates.

    Returns:
    came_from (dict): A dictionary mapping each node to the node it came from.
    cost_so_far (dict): A dictionary mapping each node to the cost of the path from the start node to it.
    """

    # Initialize the frontier with the start node
    frontier = []
    heapq.heappush(frontier, (0, start))

    # Initialize the came_from and cost_so_far dictionaries
    came_from = {start: None}
    cost_so_far = {start: 0}

    # Initialize the directions dictionary
    directions = {start: []}

    # Loop until the frontier is empty
    while frontier:
        # Pop the node with the lowest cost from the frontier
        _, current = heapq.heappop(frontier)

        # If the current node is the goal, we're done
        if current == goal:
            break

        # For each neighbor of the current node
        for next in get_neighbor_coordinates(grid, current[0], current[1]):
            # Calculate the direction to the neighbor
            new_direction = (next[0] - current[0], next[1] - current[1])

            # Add the new direction to the list of directions for the current node
            new_directions = directions[current] + [new_direction]

            # If there are more than 3 steps in the same direction, skip this neighbor
            if len(new_directions) >= 3 and all(d == new_direction for d in new_directions[-3:]):
                continue

            # If the new direction is a 180° turn, skip this neighbor
            if len(new_directions) >= 1 and new_directions[-1][0] + new_direction[0] == 0 and new_directions[-1][1] + \
                    new_direction[1] == 0:
                continue

            # Calculate the cost of the path to the neighbor through the current node
            new_cost = cost_so_far[current] + int(grid[next[0]][next[1]])

            # If the neighbor hasn't been visited yet or the new cost is lower than the previous cost
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                # Update the cost of the path to the neighbor
                cost_so_far[next] = new_cost

                # Calculate the priority of the neighbor
                priority = new_cost + manhattan_distance(goal, next)

                # Add the neighbor to the frontier with its priority
                heapq.heappush(frontier, (priority, next))

                # Update the node the neighbor came from
                came_from[next] = current

                # Update the directions to the neighbor
                directions[next] = new_directions

    # Return the came_from and cost_so_far dictionaries
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


grid = [list(map(int, line)) for line in data]
start, goal = (0, 0), (len(grid) - 1, len(grid[0]) - 1)
print(f"Start: {start}, Goal: {goal}")

# A*
came_from, cost_so_far = a_star(grid, start, goal)

# Reconstruct Path
path = reconstruct_path(came_from, start, goal)

display_path_in_grid(grid, path)

# Print the total heat loss
print(cost_so_far[goal])
