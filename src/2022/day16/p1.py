import re
from collections import deque
import itertools

from copy import deepcopy

with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

# Valve VO has flow rate=6; tunnels lead to valves KM, RF, HS, LJ, IA
# 1 min to open + 1 min to change pos
valves: list = []


class Valve:
	target_edges: dict = dict()

	def __init__(self, n, f, e):
		self.name = n
		self.flow = int(f)
		self.edges = e

	def distance(self, end):
		return bfs(self, end)

	def calc_target_distances(self):
		for t in targets:
			if t == self:
				continue
			if self.target_edges.get(t.name, -1) == -1:
				self.target_edges[t.name] = self.distance(t)
			else:
				self.target_edges[t.name] = min(self.target_edges[t.name], self.distance(t))

	def __str__(self):
		return self.name

	def __repr__(self):
		return f"Valve {self.name} ({self.flow} ppm)"

	def __lt__(self, other):
		return self.flow < other.flow

	def __gt__(self, other):
		return self.flow > other.flow

	def __eq__(self, other):
		return self.flow == other.flow


# Breadth-first search (BFS)
# Time Complexity: O(V+E), V: number of vertices, E: number of edges
def bfs(start, end):
	# 1. Pick any node, visit the adjacent unvisited vertex, mark it as visited, and insert it in a queue.
	queue = deque()
	# queue element: (pos, distance)
	queue.append((start, 0))
	visited: set(tuple) = set()
	while queue:
		node, distance = queue.popleft()
		if node.name == end.name:
			return distance
		if node.name in visited:
			continue
		visited.add(node.name)
		for move in [m for m in valves if node.name in m.edges]:
			queue.append((move, distance + 1))
	# queue is empty and no match was found
	return -1


def unreachable():
	for v in valves:
		d = v.distance(valves[0])
		if d >= 30:
			print(d, v.name)


def distances():
	for v in valves:
		print(v.distance(start_valve), v.name)

for line in data:
	name, flow_rate = re.findall("Valve ([A-Z]{2}) has flow rate=([0-9]+);", line)[0]
	edges = re.findall("[A-Z]{2}", line)[1:]
	valves.append(Valve(name, int(flow_rate), [e.strip() for e in edges]))
	if name == "AA":
		start_valve: Valve = valves[-1]

targets = [v for v in valves if v.flow > 0]
targets.sort()

routes: set = set()

def go_path(a, b, time):
	#added_time = a.target_edges[b.name] + 1
	added_time = bfs(a, b) + 1
	added_pressure = b.flow * (30 - added_time - time)
	return added_time, added_pressure


time, pressure = (0, 0)
last_p = start_valve
for p in targets:
	dt, dp = go_path(last_p, p, time)
	last_p = p
	time += dt
	pressure += dp

print(time)

exit(0)

#   permutations = itertools.permutations(targets)
#   count = 0
#   for path in permutations:
#   	count += 1
#   print(f"Total checks: {count}")

pressure_max = 0
for path in targets:
	time, pressure = (0, 0)
	last_p = start_valve
	for p in path:
		dt, dp = go_path(last_p, p, time)
		last_p = p
		if time + dt <= 30:
			time += dt
			pressure += dp
		else:
			break
	pressure_max = max(pressure_max, pressure)
	print(pressure, time)

print(pressure_max)