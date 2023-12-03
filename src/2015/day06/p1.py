import numpy as np

with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

grid = np.array(np.zeros((1000, 1000)), dtype=bool)

for line in data:
	if line.startswith("turn on"):
		line = line.removeprefix("turn on ")
		x1, y1 = line.split(" through ")[0].split(",")
		x2, y2 = line.split(" through ")[1].split(",")
		grid[int(x1):int(x2)+1, int(y1):int(y2)+1] = 1
	elif line.startswith("turn off"):
		line = line.removeprefix("turn off ")
		x1, y1 = line.split(" through ")[0].split(",")
		x2, y2 = line.split(" through ")[1].split(",")
		grid[int(x1):int(x2)+1, int(y1):int(y2)+1] = 0
	elif line.startswith("toggle"):
		line = line.removeprefix("toggle ")
		x1, y1 = line.split(" through ")[0].split(",")
		x2, y2 = line.split(" through ")[1].split(",")
		grid[int(x1):int(x2)+1, int(y1):int(y2)+1] = np.invert(grid[int(x1):int(x2)+1, int(y1):int(y2)+1])

print(np.sum(grid))
