with open("input") as file:
	data = [line.removesuffix("\n") for line in file][0]

up = data.count('(')
down = data.count(')')
print(up - down)

floor = 0
for pos, i in enumerate(data):
	floor += 1 if i == '(' else -1
	if floor == -1:
		print(pos + 1)
		break