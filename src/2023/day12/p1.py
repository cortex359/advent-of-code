import re
import numpy as np
from collections import deque
from collections import defaultdict
import itertools

# d = defaultdict(int)  # Default to int (0)

with open("example") as file:
    data: list = [line.removesuffix("\n") for line in file]

# Parsing Stuff
# -------------
number_list: list[int] = [int(line) for line in data if line.isdigit()]
grid: list[list] = [list(line) for line in data]

# Regex Stuff
# -----------
def line_to_list_of_ints(line):
    """Convert a line of numbers to a list of ints"""
    return list(map(int, re.findall(r'\d+', line)))


def get_fullstr_by_pointing_to_segment(line: str, index: int, chars: str = "01234567890", valid: bool = True) -> str:
    """Get full string of valid chars by pointing to a segment of it, expending left and right from there"""
    end = index

    while index >= 0 and ((chars.find(line[index]) >= 0 and valid) or (chars.find(line[index]) < 0 and not valid)):
        index -= 1
    while end < len(line) and ((chars.find(line[end]) >= 0 and valid) or (chars.find(line[end]) < 0 and not valid)):
        end += 1

    return line[index + 1:end]


# cartesian product
# for i, j in itertools.product('ABC', 'xyz'):
#   print('{}{}, '.format(i, j), end='')
# Ax, Ay, Az, Bx, By, Bz, Cx, Cy, Cz

# permutations
# itertools.permutations('ABCD', 2)
# AB AC AD BA BC BD CA CB CD DA DB DC

# combinations
# itertools.combinations('ABCD', 2)
# AB AC AD BC BD CD


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


# 3D Grid Stuff
# -------------
def create_3d_grid(depth, height, width, fill_value=0):
    """Create a 3D Grid with a default value"""
    return [[[fill_value for _ in range(width)] for _ in range(height)] for _ in range(depth)]


def get_3d_neighbor_coordinates(grid, x, y, z):
    """Get all valid neighbor coordinates (up to 26) in a 3D Grid"""
    neighbors = []
    for dx, dy, dz in [(i, j, k) for i in [-1, 0, 1] for j in [-1, 0, 1] for k in [-1, 0, 1] if (i, j, k) != (0, 0, 0)]:
        nx, ny, nz = x + dx, y + dy, z + dz
        if 0 <= nx < len(grid[0][0]) and 0 <= ny < len(grid[0]) and 0 <= nz < len(grid):
            neighbors.append((nx, ny, nz))
    return neighbors

def get_3d_neighbors(grid, x, y, z):
    """Get all valid neighbor values (up to 26) in a 3D Grid"""
    neighbors = []
    for _x, _y, _z in get_3d_neighbor_coordinates(grid, x, y, z):
        neighbors.append(grid[_z][_y][_x])
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


def slice_ranges(a: set[tuple[int, int]], b: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """slices a set of intervals into subintervals, such that all subintervals are either inside or outside every
    interval in set b"""
    tupels: tuple[int] = tuple()
    for i in a.union(b):
        tupels += i

    sliced_boundaries: set[tuple[int, int]] = set()
    boundary_list: list[int] = sorted(list(set(tupels)))

    for i in range(len(boundary_list) - 1):
        for s in a:
            if s[0] <= boundary_list[i] < boundary_list[i + 1] <= s[1]:
                sliced_boundaries.add((boundary_list[i], boundary_list[i + 1]))

    return sliced_boundaries

def gen_configuration(broken: int, operational: int) -> str:
    return str(itertools.repeat('#', broken)) + str(itertools.repeat('.', operational))


data = [".?????.????.#?.???? 4,3,1,1,1"]
max_num = 0
for l in data:
    s = l.split()[0]
    t = l.split()[1].split(',')

    segments: list = []
    segment_length = 0
    for i in range(len(s)):
        if s[i] == '#' or s[i] == '?':
            # enter big segment
            segment_length += 1
        if (s[i] == '.' or i == len(s)-1) and segment_length > 0:
            # leave big segment
            segments.append(segment_length)
            segment_length = 0
    # [5, 4, 2, 4]
    # .?????.????.#?.????
    # .-----.----.#-.----
    print(segments)


def test_line(line: list, counts: list) -> int:
    for

def permute_rest(line: list, index: int, stack: list, counts: list) -> int:
    if index >= len(list):
        return test_line(line)
    if line[index] == '?':
        line_a = line.copy()
        line_a[index] = '.'

        line_b = line.copy()
        line_b[index] = '#'
        if line_b[:index+1].count('#') <= stack.popleft():
            return permute_rest(line_a, index + 1, stack, counts) + permute_rest(line_b, index + 1, stack, counts)
        else:
            return permute_rest(line_a, index + 1, stack, counts)

print(list(itertools.permutations('.#', 2)))