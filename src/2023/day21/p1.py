import sys
from collections import deque

import matplotlib.pyplot as plt
import networkx as nx

file_path = sys.argv[1] if len(sys.argv) > 1 else 'input'

with open(file_path) as file:
    data: list = [line.removesuffix("\n") for line in file]

grid: list[list] = [list(line) for line in data]


def get_neighbor_coordinates(grid, zeile: int, spalte: int) -> list[tuple[int, int]]:
    """Get all cross neighbor coordinates in a 2D Grid"""
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = zeile + dx, spalte + dy
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
            neighbors.append((nx, ny))
    return neighbors


# garden plots: .
# rocks:        #
# start pos:    S (garden plot)
start = [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == 'S'][0]
print(f"Starting position: {start}")


def create_graph_from_grid(grid: list[list], start: tuple[int, int]) -> dict[tuple[int, int], list[tuple[int, int]]]:
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


def visualize_graph(graph: dict[tuple[int, int], list[tuple[int, int]]], reachable_nodes: set[tuple[int, int]]):
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

    # nx.draw(G, pos=nx.spring_layout(G, fixed=[(5,5)], pos=initial_pos),  with_labels=True, font_size=8, node_size=1000, node_color='skyblue', edge_color='black')
    # nx.draw(G, pos=initial_pos, with_labels=True, font_size=8, node_size=500, node_color='skyblue', edge_color='black')

    if file_path == 'input':
        plt.figure(figsize=(100, 100))

    options = {"edgecolors": "tab:gray", "node_size": 800, "alpha": 0.9, "node_size": 500}
    nx.draw_networkx_nodes(G, pos=initial_pos, nodelist=reachable_nodes, node_color='skyblue', **options)
    nx.draw_networkx_nodes(G, pos=initial_pos, nodelist=unreachable_nodes, node_color='red', **options)
    nx.draw_networkx_edges(G, pos=initial_pos, width=1.0, alpha=0.5, edge_color='black')
    nx.draw_networkx_labels(G, pos=initial_pos, font_size=8, font_color='black')

    plt.tight_layout()
    plt.axis("off")
    if file_path == 'input':
        plt.savefig('graph.pdf')
    else:
        plt.show()


def make_graph_with_nx(grid: list[list], start: tuple[int, int]) -> nx.Graph:
    G = nx.Graph()
    position = start
    for m in range(len(grid)):
        for n in range(len(grid[0])):
            if grid[m][n] == '.' or grid[m][n] == 'S':
                G.add_node((m, n)) if grid[m][n] != 'S' else G.add_node((m, n), start=True)
                G.add_edges_from([((m, n), neighbor) for neighbor in get_neighbor_coordinates(grid, m, n) if
                                  grid[neighbor[0]][neighbor[1]] == '.'])
    return G


def visualize_nx_graph(graph: nx.Graph):
    initial_pos = {}
    for g in G.nodes:
        initial_pos[g] = (g[1], -g[0])

    if file_path == 'input':
        plt.figure(figsize=(100, 100))
    nx.draw(G, pos=initial_pos, with_labels=True, font_size=8, node_size=800, node_color='skyblue', edge_color='black')

    plt.tight_layout()
    plt.axis("off")
    if file_path == 'input':
        plt.savefig('graph.pdf')
    else:
        plt.show()


# ungewichtet, zyklisch und ungerichtet
# G = make_graph_with_nx(grid, start)
# visualize_nx_graph(G)

## Not computable
def path_of_length_exists(graph, start, end, length):
    queue = deque([(start, 0)])
    while queue:
        vertex, level = queue.popleft()
        if vertex == end and level == length:
            return True
        if level < length:
            for neighbor in graph[vertex]:
                queue.append((neighbor, level + 1))
    return False


def get_reachables(graph, start, length):
    visited, queue = set(), deque([(start, 0)])
    reachable_nodes = set()
    while queue:
        vertex, level = queue.popleft()

        if vertex not in visited:
            visited.add(vertex)
            if level <= length:
                if (level + 1) % 2:
                    reachable_nodes.add(vertex)
                for n in set(graph[vertex]) - visited:
                    queue.append((n, level + 1))
    return reachable_nodes


steps = 64
graph = create_graph_from_grid(grid, start)

print(f"Graph initialized with {len(graph)} nodes. Checking for nodes reachable in exactly {steps} steps...")

reachable_nodes = get_reachables(graph, start, steps)
print(f"Number of reachable nodes, exactly {steps} steps away from {start}: {len(reachable_nodes)}")

# visualize_graph(graph, reachable_nodes)
