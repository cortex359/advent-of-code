from collections import deque
import numpy as np

with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

cubes = np.array([[[0] * 23] * 23] * 23)
cube_faces = np.array([[[0] * 23] * 23] * 23)
for line in data:
	x, y, z = map(int, line.split(","))
	cubes[z, y, x] = 1
	cube_faces[z, y, x] = 6
	for d in (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1):
		dx, dy, dz = d
		if cube_faces[z + dz, y + dy, x + dx] > 0:
			cube_faces[z + dz, y + dy, x + dx] -= 1
			cube_faces[z, y, x] -= 1

print("Faces:", cube_faces.sum())


def is_pocket(x, y, z):
	queue = deque()
	queue.append((x, y, z))
	visited: set[tuple] = {x, y, z}
	while queue:
		x, y, z = queue.popleft()
		if min(x, y, z) < 0 or max(x, y, z) > 21:
			return False

		for adjecents in (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1):
			dx, dy, dz = adjecents
			nx, ny, nz = (x + dx, y + dy, z + dz)
			if (nx, ny, nz) not in visited and cubes[nz, ny, nx] == 0:
				queue.append((nx, ny, nz))
				visited.add((nx, ny, nz))
	return True


pockets = set()
for x in range(23):
	for y in range(23):
		for z in range(23):
			if cubes[z, y, x] == 0:
				if is_pocket(x, y, z):
					pockets.add((x, y, z))

print(f"Found {len(pockets)} pockets of air to be excluded.")

cube_exterior_faces = np.array([[[0] * 23] * 23] * 23)

for line in data:
	x, y, z = map(int, line.split(","))
	cube_exterior_faces[z, y, x] = 6
	for d in (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1):
		dx, dy, dz = d
		if cube_exterior_faces[z + dz, y + dy, x + dx] > 0:
			cube_exterior_faces[z + dz, y + dy, x + dx] -= 1
			cube_exterior_faces[z, y, x] -= 1
		elif (x + dx, y + dy, z + dz) in pockets:
			cube_exterior_faces[z, y, x] -= 1

print("Exterior surface area:", cube_exterior_faces.sum())
