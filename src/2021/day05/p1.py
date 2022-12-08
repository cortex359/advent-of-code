import numpy as np

with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

diagram = np.zeros(1000000, int).reshape(1000, 1000)
#diagram = np.zeros(100, int).reshape(10, 10)

for line in data:
	start, end = line.split(" -> ")
	x1, y1 = map(int, start.split(","))
	x2, y2 = map(int, end.split(","))
	print(f"{x1}, {y1}, {x2}, {y2}")

	xs = min(x1, x2)
	xm = max(x1, x2)
	ys = min(y1, y2)
	ym = max(y1, y2)

	if x1 == x2:
		for y in range(ys, ym+1):
			diagram[y, x1] += 1
	elif y1 == y2:
		for x in range(xs, xm+1):
			diagram[y1, x] += 1
	else:
		x = xs
		y = ys
		while x1 != x2 and y1 != y2:
			diagram[y1, x1] += 1
			if x1 < x2:
				x1 += 1
			else:
				x1 -= 1
			if y1 < y2:
				y1 += 1
			else:
				y1 -= 1
		diagram[y1, x1] += 1

print(len([x for x in diagram.flatten().tolist() if x >= 2]))
