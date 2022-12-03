with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

horiz = 0
depth = 0
aim = 0

for l in data:
	if l.startswith("forward"):
		horiz += int(l.split()[1])
		depth += (aim * int(l.split()[1]))
	elif l.startswith("down"):
		#depth += int(l.split()[1])
		aim += int(l.split()[1])
	elif l.startswith("up"):
		#depth -= int(l.split()[1])
		aim -= int(l.split()[1])

print("Horizontal: " + str(horiz))
print("Depth: " + str(depth))
print("Aim: " + str(aim))
print("Product: " + str(horiz * depth))