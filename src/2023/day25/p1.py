import sys

import matplotlib.pyplot as plt
import networkx as nx
import pyvis as pv


file_path = sys.argv[1] if len(sys.argv) > 1 else 'input'

with open(file_path) as file:
    data: list = [line.removesuffix("\n") for line in file]

G = nx.Graph()
for line in data:
    component, cl = line.split(": ")
    connections = cl.split(" ")
    G.add_node(component)
    for c in connections:
        G.add_edge(component, c, capacity=1)


plt.figure(figsize=(100, 100))
nx.draw(G, with_labels=True, font_size=4, node_size=800, node_color='skyblue', edge_color='black')
plt.savefig('graph.pdf')

# nodes must be from different clusters
cut_value, partition = nx.minimum_cut(G, "fss", "bpr")
print(f"cut_value: {cut_value}")
print(f"partitions: {partition}")
print(f"partition length: {len(partition[0])}, {len(partition[1])}")
print(f"puzzle answer: {len(partition[0]) * len(partition[1])}")

got_net = pv.network.Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
got_net.from_nx(G)
#got_net.force_atlas_2based(gravity=-30)
got_net.show("graph.html", notebook=False)
