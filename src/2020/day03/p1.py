with open("input") as file:
	data = [line.removesuffix("\n") for line in file]


def transverse(right=3, d=1):
	# . open squares
	# # trees
	x = 0
	trees = 0
	for i in range(len(data)):
		if i < d or i % d != 0:
			continue
		line = data[i]
		x += right
		if line[x % len(line)] == '#':
			trees += 1
	return trees

product = 1
for r, d in (1, 1), (3, 1), (5, 1), (7, 1), (1, 2):
	product *= transverse(r, d)

print(product)
