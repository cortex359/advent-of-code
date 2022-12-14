import numpy as np

with open("input") as file:
	# with open("example") as file:
	data = [line.removesuffix("\n") for line in file]

sand_start = (500, 0)
rock: list[(int, int)] = []
rock_formations: list[list[(int, int)]] = []

# 455 < x < 526
# 15 < y < 170

grid = np.array([['.'] * 550] * 180)


# 498,4 -> 498,6 -> 496,6
def draw_rocks(rf):
	for i in range(len(rf) - 1):
		ax, ay = rf[i]
		bx, by = rf[i + 1]

		if ax == bx:
			# vertical
			if by < ay:
				y = ay
				ay = by
				by = y
			for s in range(ay, by + 1):
				grid[s, ax] = "#"
		elif ay == by:
			# horizontal
			if bx < ax:
				x = ax
				ax = bx
				bx = x
			for s in range(ax, bx + 1):
				grid[ay, s] = "#"
		else:
			print(f"Error on {ax}:{ay} -> {bx}{by}.\n")


# - A unit of sand always falls down one step if possible.
#   - if immediately below is blocked,  the unit of sand attempts
#   - to instead move diagonally one step down and to the left
#   - if blocked, instead move diagonally one step down and to the right
#
# move down, then down-left, then down-right, then stop and create next unit at source
#
def move_diag(x, y):
	# move diagonally one step down and to the left
	delta_xy = 1
	if grid[y + delta_xy, x - delta_xy] == ".":
		y += delta_xy
		x -= delta_xy
		return x, y
	else:
		return move_diag_right(x, y)


def move_diag_right(x, y):
	# move diagonally one step down and to the right
	delta_xy = 1
	if grid[y + delta_xy, x + delta_xy] == ".":
		y += delta_xy
		x += delta_xy
	return x, y


def move_down(x, y):
	# sand always falls down one step if possible
	delta_y = 0
	while grid[y + delta_y, x] == ".":
		delta_y += 1
	delta_y -= 1
	y += delta_y
	return x, y


def draw_sand():
	x, y = sand_start
	# delete sand
	grid[y, x] = "."

	x, y = move_down(x, y)
	x, y = move_diag(x, y)

	# place down
	if grid[y, x] != '.':
		print(f"Error at x={x}, y={y}!\n")
	else:
		grid[y, x] = "o"


for line in data:
	rock = [tuple(map(int, x.split(","))) for x in line.split(" -> ")]
	rock_formations.append(rock)

for rock in rock_formations:
	draw_rocks(rock)

# Void border
grid[-1] = ["~"] * 550

while "o" not in grid[-2]:
	draw_sand()

# mark sand source after sand has been drawn!
grid[sand_start[1], sand_start[0]] = "+"

# Display grid
for l in grid:
	for i, m in enumerate(l):
		if 450 < i < 550:
			print(m, end='')
	print()
