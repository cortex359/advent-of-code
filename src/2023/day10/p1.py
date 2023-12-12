from collections import deque

with open("input") as file:
    data: list = [line.removesuffix("\n") for line in file]

grid: list[list] = [list(line) for line in data]

# 2D Grid Stuff
# -------------
def get_neighbor_coordinates(grid, zeile: int, spalte: int) -> list[tuple[int, int]]:
    """Get all cross neighbor coordinates in a 2D Grid"""
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = zeile + dx, spalte + dy
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
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


def rotate_grid(grid):
    """Rotate a 2D Grid 90 degrees clockwise"""
    return [list(reversed(col)) for col in zip(*grid)]

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

print('Starting at', start_position)
grid_distances = grid.copy()

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
        print(neighbor)
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

#for g in grid_distances:
#    print(''.join(map(str, g)))

max_distance = 0
for m in range(len(grid_distances)):
    for n in grid_distances[m]:
        if type(n) is int:
            max_distance = max(max_distance, n)

print("Max Distance:", max_distance)