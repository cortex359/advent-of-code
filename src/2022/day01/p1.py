with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

calories = 0
elves = []
for line in data:
	if line == "":
		elves.append(calories)
		calories = 0
	else:
		calories += int(line)

print(sorted(elves)[-1])
print(sum(sorted(elves)[-3:]))