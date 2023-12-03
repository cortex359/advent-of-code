with open("input") as file:
	data = [line.removesuffix("\n") for line in file][0]


x, y = 0, 0
locations: list[(int, int)] = []
locations.append((x, y))
count_p1 = 1
for direction in data:
	if direction == '>':
		x += 1
	elif direction == '<':
		x -= 1
	elif direction == '^':
		y += 1
	else:
		y -= 1

	if locations.count((x, y)) == 0:
		count_p1 += 1
		locations.append((x, y))


x_santa, y_santa = 0, 0
x_robo, y_robo = 0, 0
locations: list[(int, int)] = []
locations.append((0, 0))
count_p2 = 1
for i in range(len(data)):
	if i %2 == 1:
		continue
	santa = data[i]
	robo = data[i+1]
	if santa == '>':
		x_santa += 1
	elif santa == '<':
		x_santa -= 1
	elif santa == '^':
		y_santa += 1
	else:
		y_santa -= 1

	if robo == '>':
		x_robo += 1
	elif robo == '<':
		x_robo -= 1
	elif robo == '^':
		y_robo += 1
	else:
		y_robo -= 1

	if locations.count((x_santa, y_santa)) == 0:
		count_p2 += 1
		locations.append((x_santa, y_santa))

	if locations.count((x_robo, y_robo)) == 0:
		count_p2 += 1
		locations.append((x_robo, y_robo))

print(count_p1)
print(count_p2)