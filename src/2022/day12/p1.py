from copy import deepcopy
from collections import deque

with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

heights = "abcdefghijklmnopqrstuvwxyzSE"

start_pos = (0, 0)
end_pos = (0, 0)

heightmap: list[list[int]] = [[heights.index(c) for c in list(line)] for line in data]

for r, row in enumerate(heightmap):
	for c, col in enumerate(row):
		if col == 26:
			start_pos = (r, c)
			heightmap[r][c] = 0
		elif col == 27:
			end_pos = (r, c)
			# z = 25
			heightmap[r][c] = 25


def possible_moves(hmap, pos):
	r, c = pos
	h = hmap[r][c]
	moves = []
	if r != 0:
		up = hmap[r - 1][c]
		if h + 1 >= up:
			moves.append((r - 1, c))
	if c != 0:
		left = hmap[r][c - 1]
		if h + 1 >= left:
			moves.append((r, c - 1))
	if c < len(hmap[r]) - 1:
		right = hmap[r][c + 1]
		if h + 1 >= right:
			moves.append((r, c + 1))
	if r < len(hmap) - 1:
		down = hmap[r + 1][c]
		if h + 1 >= down:
			moves.append((r + 1, c))
	return moves


def recursive_evaluate_moves(hmap, visited: list[(int, int)], pos: (int, int)):
	visited.append(pos)
	global path_length
	if len(visited) > path_length:
		# print("Ignoring")
		return
	if pos == end_pos:
		if len(visited) < path_length:
			path_length = len(visited)
			global min_path
			min_path = deepcopy(visited)
		print(f"Path found after {len(visited)} moves: {visited}")
		return
	pm = possible_moves(hmap, pos)
	if len(pm) == 0:
		# print("Dead end")
		return
	for m in pm:
		if visited.count(m) == 0:
			recursive_evaluate_moves(hmap, deepcopy(visited), m)


# Breadth-first search (BFS)
# Time Complexity: O(V+E), V: number of vertices, E: number of edges
def bfs(hmap, start, end):
	# 1. Pick any node, visit the adjacent unvisited vertex, mark it as visited, and insert it in a queue.
	queue = deque()
	# queue element: (pos, distance)
	queue.append((start, 0))
	visited: set(tuple) = set()
	while queue:
		pos, distance = queue.popleft()
		if pos == end:
			return distance
		if pos in visited:
			continue
		visited.add(pos)
		for move in possible_moves(hmap, pos):
			queue.append((move, distance + 1))
	# queue is empty and no match was found
	return -1


# works only with example
#   visited: list[(int, int)] = [start_pos]
#   path_length: int = 999999
#   min_path: list[(int, int)] = []
#   recursive_evaluate_moves(map, visited, start_pos)
#   print(f"Shortest path: {path_length}")

# Part 1
steps = bfs(heightmap, start_pos, end_pos)
print(f"Fewest steps required to move from S = {start_pos} to E = {end_pos}:\n\t{steps:4n}")


min_distance = float("inf")
min_start_pos: (int, int)
for r, row in enumerate(heightmap):
	for c, col in enumerate(row):
		if col == 0:
			distance = bfs(heightmap, (r, c), end_pos)
			if distance != -1:
				if min_distance > distance:
					min_distance = distance
					min_start_pos = (r, c)
				#print(f"{distance:4n}: Start: {r:3n}:{c:3n}, distance: {distance:4n}")

print(f"Fewest steps required from closest point with elevation a {min_start_pos} to E = {end_pos}:\n\t{min_distance:4n}")
