import numpy as np

with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

ranges: list[list[bool, int, int, int, int, int, int]] = []
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
	ranges.append([state, x_from, x_to, y_from, y_to, z_from, z_to])

print(ranges[0])


def contains(r: list[bool, int, int, int, int, int, int], s: list[bool, int, int, int, int, int, int]):
	a_1, a_2, b_1, b_2, c_1, c_2 = r[1:]
	x_1, x_2, y_1, y_2, z_1, z_2 = s[1:]
	if a_2 <= x_2 and a_1 >= x_1:
		if b_2 <= y_2 and b_1 >= y_1:
			if c_2 <= z_2 and c_1 >= z_1:
				return True

def intersects(r: list[bool, int, int, int, int, int, int], s: list[bool, int, int, int, int, int, int]):
	a_1, a_2, b_1, b_2, c_1, c_2 = r[1:]
	x_1, x_2, y_1, y_2, z_1, z_2 = s[1:]
	if a_1 <= x_1 <= a_2 or a_1 <= x_2 <= a_2:
		if b_1 <= y_1 <= b_2 or b_1 <= y_2 <= b_2:
			if c_1 <= z_1 <= c_2 or c_1 <= z_2 <= c_2:
				return True

def intersection(r: list[bool, int, int, int, int, int, int], s: list[bool, int, int, int, int, int, int]):
	a_1, a_2, b_1, b_2, c_1, c_2 = r[1:]
	x_1, x_2, y_1, y_2, z_1, z_2 = s[1:]
	if x_1 <= a_1 <= x_2:
		if x_1 <= a_2 <= x_2:




def volume(r: list[bool, int, int, int, int, int, int]):
	x_1, x_2, y_1, y_2, z_1, z_2 = r[1:]
	if r[0]:
		sign = 1
	else:
		sign = -1
	return (x_2 - x_1) * (y_2 - y_1) * (z_2 - z_1) * sign


contain_counter = 0
for r in ranges:
	intersect_counter = 0
	for s in ranges:
		if r != s:
			if contains(r, s):
				contain_counter += 1
			if intersects(r, s):
				intersect_counter += 1
	if intersect_counter == 22:
		print(r)
	print(intersect_counter)

print(contain_counter)
