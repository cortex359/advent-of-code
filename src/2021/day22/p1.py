import numpy as np

with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

ranges: list[list[bool, range, range, range]] = []
for seq in data:
	state = 1 if seq.split()[0] == "on" else 0
	for dimension in seq.split()[1].split(","):
		if dimension.startswith("x="):
			x_from = int(dimension[2:].split("..")[0])
			x_to = int(dimension[2:].split("..")[1])
		elif dimension.startswith("y="):
			y_from = int(dimension[2:].split("..")[0])
			y_to = int(dimension[2:].split("..")[1])
		elif dimension.startswith("z="):
			z_from = int(dimension[2:].split("..")[0])
			z_to = int(dimension[2:].split("..")[1])
	ranges.append([state, range(x_from, x_to), range(y_from, y_to), range(z_from, z_to)])

print(ranges[0])

# Parsing
for r in ranges:


print(cube.sum())
