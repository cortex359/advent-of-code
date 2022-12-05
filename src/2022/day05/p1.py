from copy import deepcopy

with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

crates = 0
for line in data:
	if line != "":
		crates += 1
	else:
		break

no_of_crates = int(data[crates-1].split()[-1])

stack: list[list[str]] = []
stack_2: list[list[str]] = []

for c in range(0, no_of_crates):
	elements = []
	for line in data[:crates-1]:
		if len(line) >= c*4+1:
			if line[(c*4)+1] != " ":
				elements.append(line[(c*4)+1])
	elements.reverse()
	stack.append(elements)

# deepcopy
stack_2 = deepcopy(stack)

for line in data[crates+1:]:
	size = int(line.split()[1])
	src = int(line.split()[3]) - 1
	dest = int(line.split()[5]) - 1

	for s in range(size):
		stack[dest].append(stack[src][-1])
		stack[src].pop()

	pickup_stack = []
	pickup_stack = stack_2[src][size*-1:]

	for ps in pickup_stack:
		stack_2[dest].append(ps)
		stack_2[src].pop()

output_cm9000 = ""
for s in stack:
	output_cm9000 += s[-1]

output_cm9001 = ""
for s in stack_2:
	output_cm9001 += s[-1]

print(f"Crates on top after using CrateMover 9000: {output_cm9000}")
print(f"Crates on top after using CrateMover 9001: {output_cm9001}")