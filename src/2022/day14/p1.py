import numpy as np

with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

sand_start = (500, 0)
rock: list[(int, int)] = []
rock_formations: list[list[(int, int)]] = []

# 455 < x < 526
# 15 < y < 170

grid = np.array([['.'] * 1200] * 173)


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
	delta_y = 1
	while grid[y + delta_y, x] == ".":
		delta_y += 1
	delta_y -= 1
	y += delta_y
	return x, y


def draw_sand():
	x, y = sand_start
	# delete sand
	grid[y, x] = "."

	prev_x, prev_y = (-1, -1)

	while prev_x != x and prev_y != y:
		prev_x, prev_y = x, y
		# print(f"{prev_x}:{prev_y} -> {x}:{y}")
		x, y = move_down(x, y)
		x, y = move_diag(x, y)

	# place down
	if grid[y, x] != '.':
		print(f"Error at x={x}, y={y}!\n")
	else:
		grid[y, x] = "o"


def display_grid():
	# mark sand source after sand has been drawn!
	grid[sand_start[1], sand_start[0]] = "+"

	for c, cols in enumerate(grid):
		if 0 < c < 172:
			for r, cell in enumerate(cols):
				if 300 < r < 460:
					print(cell, end='')
			print()

###
### START
###

for line in data:
	rock = [tuple(map(int, x.split(","))) for x in line.split(" -> ")]
	rock_formations.append(rock)

for rock in rock_formations:
	draw_rocks(rock)

# Void border
# grid[-1] = ["~"] * 550
grid[170 + 2] = ["~"] * 1200


# >>>>>>-------<<<<<<
#       PART  I
# >>>>>>-------<<<<<<
# >>> 838
#
while "o" not in grid[170 + 1]:
	draw_sand()

# exclude the detected sand unit at the void border
units_of_sand = len([c for c in grid.flatten() if c == "o"]) - 1
print("Part I:", units_of_sand)


# >>>>>>-------<<<<<<
#       PART II
# >>>>>>-------<<<<<<
# >>> 27539
#
while grid[sand_start[1], sand_start[0]] != "o":
	draw_sand()

# dont exclude the sand unit
units_of_sand = len([c for c in grid.flatten() if c == "o"])
print("Part II:", units_of_sand)

display_grid()
