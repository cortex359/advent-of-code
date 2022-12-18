import re
import sys
from collections import deque
import itertools
import time as timelib

from copy import deepcopy

if "-i" in sys.argv:
	target = "input"
else:
	target = "example"

with open(target) as file:
	data = [line.removesuffix("\n") for line in file]
print(f"Loaded {target} file with {len(data)} lines.\n")


# Valve VO has flow rate=6; tunnels lead to valves KM, RF, HS, LJ, IA
# 1 min to open + 1 min to change pos
class Valve:
	target_edges: dict = dict()

	def get_edges(self):
		return [valves[e] for e in self.edges]

	def __init__(self, n: str, f, e: list[str]):
		self.name = n
		self.flow = int(f)
		self.edges = e
		self.open = False

	def distance(self, end):
		return bfs(self, end)

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


bfs_cache = dict()


# Breadth-first search (BFS)
# Time Complexity: O(V+E), V: number of vertices, E: number of edges
def bfs(start, end):
	cache = bfs_cache.get(start.name + end.name, -1)
	if cache != -1:
		return cache
	# 1. Pick any node, visit the adjacent unvisited vertex, mark it as visited, and insert it in a queue.
	queue = deque()
	# queue element: (pos, distance)
	queue.append((start, 0))
	visited: set(tuple) = set()
	while queue:
		node, distance = queue.popleft()
		if node.name == end.name:
			bfs_cache[start.name + end.name] = distance
			return distance
		if node.name in visited:
			continue
		visited.add(node.name)
		for move in valves[node.name].get_edges():
			queue.append((move, distance + 1))
	# queue is empty and no match was found
	return -1


def unreachable():
	for v in valves.values():
		d = v.distance(valves["AA"])
		if d >= 30:
			print(d, v.name)


def distances():
	for n, v in valves.items():
		print(n, v.distance(start_valve))


def output_graph_data(graph: list[Valve]):
	for g in graph:
		# print(f"{g.name}")
		for e in g.edges:
			print(f"{g.name}->{e}")


def go_path(a, b, time):
	# added_time = a.target_edges[b.name] + 1
	added_time = bfs(a, b) + 1
	added_pressure = b.flow * (30 - added_time - time)
	return added_time, added_pressure


def go_route(route: list[Valve]):
	time, pressure, position = (0, 0, valves["AA"])
	transversed = [position]
	for v in route:
		dt, dp = go_path(position, v, time)
		if time + dt > 30:
			print(f"Stopping at position {position.name}, because next valve {v.name} is {dt} min away.")
			break
		time += dt
		pressure += dp
		position = v
		transversed.append(position)
	print(f"Transversed route in {time} minutes; {pressure} pressure units released in 30 minutes.")
	print(f"Route: {transversed}")


execution_time: dict = dict()
execution_time["start"] = timelib.time()

valves: dict = dict()
targets: dict = dict()

for line in data:
	name, flow_rate = re.findall("Valve ([A-Z]{2}) has flow rate=([0-9]+);", line)[0]
	edges = re.findall("[A-Z]{2}", line)[1:]
	v = Valve(name, int(flow_rate), edges)
	valves[name] = v
	if v.flow > 0: targets[name] = v

start_valve: Valve = valves["AA"]

execution_time["parsing and setup"] = timelib.time()


def search_permutations():
	max_search_space = 1_307_674_368_000
	count = 0
	pressure_max = 0
	for path in itertools.permutations(targets):
		time, pressure = (0, 0)
		last_p = start_valve
		count += 1
		for p in path:
			dt, dp = go_path(last_p, p, time)
			last_p = p
			if time + dt <= 30:
				time += dt
				pressure += dp
			else:
				break
		pressure_max = max(pressure_max, pressure)
		if count % 10_000 == 0:
			print(f"{count:,} execution time so far: {(timelib.time() - st) * 1000:20.6f} ms\n")
			print("pressure_max:", pressure_max, "pressure/time example:", pressure, time)

	print("Finished!!!")
	print(pressure_max)


def extend_path(a, b):
	pass


# choose nearest, on tie: choose most delta pressure
def nearest_max_pressure_route():
	time, pressure = (0, 0)
	pos = valves["AA"]

	# visited = set(pos)
	while time < 30:
		options = [(t, *go_path(pos, t, time)) for t in targets.values() if not t.open]
		if not options:
			break
		# sort by delta time and then by delta pressure
		options.sort(key=lambda n: n[1] * 1000 - n[2])
		pos, dt, dp = options[0]
		if time + dt <= 30:
			time += dt
			pressure += dp
			pos.open = True
			print(pos, time, pressure)
	print("Finished.")


# choose most delta pressure
def max_delta_pressure_route():
	time, pressure = (0, 0)
	pos = valves["AA"]

	# visited = set(pos)
	while time < 30:
		# HH 12 1423
		options = [(t, *go_path(pos, t, time)) for t in targets.values() if not t.open]
		if not options:
			break
		# sort by delta pressure
		options.sort(key=lambda n: n[2] / n[1])
		if len(options) > 2:
			pos, dt, dp = options[-2]
			print(f" 2[{pos}] dp/dt: {(dp/dt)}")
		pos, dt, dp = options[-1]
		print(f" 1[{pos}] dp/dt: {(dp/dt)}")
		if time + dt <= 30:
			time += dt
			pressure += dp
			pos.open = True
			route.append(pos)
			print(pos, time, pressure)
	print("Finished.")


# count steps to highest delta pressure gain
# search all combinations with less steps
def heuristic_1_route():
	time, pressure = (0, 0)
	pos = valves["AA"]

	# visited = set(pos)
	while time < 30:
		options = [(t, *go_path(pos, t, time)) for t in targets.values() if not t.open]
		if not options: break
		# sort by delta pressure
		options.sort(key=lambda n: n[2])
		pos, dt, dp = options[-1]
		for alternatives in [o for o in options if o[1] < dt]:
			options = [(t, *go_path(alternatives, t, time)) for t in targets.values() if not t.open]
		if time + dt <= 30:
			time += dt
			pressure += dp
			pos.open = True
			route.append(pos)
			print(pos, time, pressure)
	print("Finished.")


def heuristic_2_route(pos=valves["AA"], time=0, pressure=0):
	# visited = set(pos)
	if time < 30:
		# HH 12 1423
		options = [(t, *go_path(pos, t, time)) for t in targets.values() if not t.open]
		if not options:
			return
		# sort by delta pressure
		options.sort(key=lambda n: n[2] / n[1], reverse=True)
		for opt in options:
			pos, dt, dp = opt
			print(f" 1[{pos}] dp/dt: {(dp/dt)}")
			if time + dt <= 30:
				time += dt
				pressure += dp
				pos.open = True
				print(pos, time, pressure)
				return pos + heuristic_2_route(pos, time, pressure)
	else:
		return

# >>>>>>-------<<<<<<
#       PART  I
# >>>>>>-------<<<<<<
# >>> 1737

# >>>>>>-------<<<<<<
#       PART II
# >>>>>>-------<<<<<<
# >>> 2216

route: list[Valve] = []
max_delta_pressure_route()
execution_time["max_pressure_route"] = timelib.time()

print("----")
go_route(route)
execution_time["go route"] = timelib.time()

### Timing Stats ###
execution_time["end"] = timelib.time()
for key, et in execution_time.items():
	if key == "start":
		st = execution_time["start"]
		lt = st
		continue
	elif key == "end":
		print(f"{'-' * 47}")
		lt = st
		key = "total execution time"
	print(f"{key:>30}: {(et - lt) * 1000:12.6f} ms")
	lt = et
