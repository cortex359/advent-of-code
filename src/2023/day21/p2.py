import sys
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from numpy.polynomial import Polynomial

file_path = sys.argv[1] if len(sys.argv) > 1 else 'input'

with open(file_path) as file:
    data: list = [line.removesuffix("\n") for line in file]


def get_neighbor_coordinates(grid, zeile: int, spalte: int) -> list[tuple[int, int]]:
    """Get all cross neighbor coordinates in a 2D Grid"""
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = zeile + dx, spalte + dy
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            neighbors.append((nx, ny))
    return neighbors


def create_graph_from_grid(grid: [list[list], np.ndarray], start: tuple[int, int]) -> dict[tuple[int, int], list[tuple[int, int]]]:
    """Create a Graph from a 2D Grid"""
    graph: dict[tuple[int, int], list[tuple[int, int]]] = {}
    visited, queue = set(), deque([start])
    while queue:
        vertex = queue.popleft()
        for n in [n for n in get_neighbor_coordinates(grid, vertex[0], vertex[1]) if grid[n[0]][n[1]] == '.']:
            if n not in visited:
                visited.add(n)
                queue.append(n)
                if vertex not in graph:
                    graph[vertex] = []
                if n not in graph:
                    graph[n] = []
                graph[vertex].append(n)
                graph[n].append(vertex)
    return graph


def visualize_graph(graph: dict[tuple[int, int], list[tuple[int, int]]], reachable_nodes: set[tuple[int, int]], save_path: str = None):
    """Visualize a directed graph with Matplotlib"""
    G = nx.Graph()
    unreachable_nodes = set(graph.keys()) - reachable_nodes
    for node, neighbors in graph.items():
        G.add_node(node)
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # transform [row, col] notation to x, y positions
    initial_pos = {}
    for g in graph:
        initial_pos[g] = (g[1], -g[0])

    if save_path:
        plt.figure(figsize=(100, 100))

    options = {"edgecolors": "tab:gray", "node_size": 800, "alpha": 0.9, "node_size": 500}
    nx.draw_networkx_nodes(G, pos=initial_pos, nodelist=reachable_nodes, node_color='skyblue', **options)
    nx.draw_networkx_nodes(G, pos=initial_pos, nodelist=unreachable_nodes, node_color='red', **options)
    nx.draw_networkx_edges(G, pos=initial_pos, width=1.0, alpha=0.5, edge_color='black')
    nx.draw_networkx_labels(G, pos=initial_pos, font_size=8, font_color='black')

    plt.tight_layout()
    plt.axis("off")
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

def get_reachables(G, start, length):
    len_modulo = length % 2
    visited, queue = set(), deque([(start, 0)])
    reachable_nodes = set()
    while queue:
        vertex, level = queue.popleft()

        if vertex not in visited:
            visited.add(vertex)
            if level <= length:
                if level % 2 == len_modulo:
                    reachable_nodes.add(vertex)
                for n in set(G[vertex]) - visited:
                    queue.append((n, level + 1))
    return reachable_nodes

def run_simulation(si: int, np_grid, start):
    steps = 65 + si * 131

    grid_expansions = ((steps - start[0]) // len(grid) + 1) * 2 + 1
    #print(f"Expanding grid {grid_expansions} times in both directions")

    super_grid = np.tile(np_grid, (grid_expansions, grid_expansions))
    start = (start[0] + (grid_expansions//2) * len(grid), start[1] + (grid_expansions//2) * len(grid[0]))
    #print(f"New starting position {start} in a {len(super_grid)}x{len(super_grid[0])} grid")
    graph = create_graph_from_grid(super_grid, start)
    #print(f"Graph initialized with {len(graph)} nodes. Checking for nodes reachable in exactly {steps} steps...")
    reachable_nodes = get_reachables(graph, start, steps)
    #print(f"Number of reachable nodes, exactly {steps} steps away from {start}: {len(reachable_nodes)}")

    # markdown table:
    #print(f"| {si} | {steps} | {start} | {len(super_grid)}x{len(super_grid[0])} | {len(reachable_nodes)} |")
    return len(reachable_nodes)


# garden plots: .
# rocks:        #
grid: list[list] = [list(line) for line in data]

# start pos:    S (garden plot)
start = [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == 'S'][0]
#print(f"Original starting position {start} in a {len(grid)}x{len(grid[0])} grid")

# normalize grid after original startposition has been determined
grid[start[0]][start[1]] = '.'
np_grid = np.array(grid)

# get a 2nd order polynomial fit with the first 3 points
degree = 2
plot_numbers = np.zeros(degree + 1, dtype=np.int_)
for i in range(degree + 1):
    plot_numbers[i] = run_simulation(i, np_grid, start)

print(f"First 3 garden plot numbers: {plot_numbers}")

print(f"Solving linear equation system for {degree + 1} unknown...")
X = np.array(list(range(degree + 1)), dtype=np.int_)
A = np.array([X**i for i in range(degree + 1)]).T
b = np.array(plot_numbers, dtype=np.int_)

poly = Polynomial(np.linalg.solve(A, b), symbol='i')
print(f"Matching polynomial for given sequence {poly}")

target_steps = 26501365
i = (target_steps - start[0]) // np_grid.shape[0]
print(f"with i = {i:,} for {target_steps:,} steps, we get the total number of garden plots that can be visited:")
print(f"{int(poly(i))}")
