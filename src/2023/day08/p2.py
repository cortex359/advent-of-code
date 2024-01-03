import itertools
import math

with open("input") as file:
    data: list = [line.removesuffix("\n") for line in file]

instructions = list(data[0].strip())
network: dict = {}

for line in [l for l in data[1:] if l != ""]:
    line = line.replace("(", "").replace(")", "")
    node = line.split(" = ")[0]
    l, r = line.split(" = ")[1].split(", ")
    network[node] = (l, r)


def count_steps_to_z(pos):
    """Counts the steps needed to reach an element ending on 'Z'"""
    counter = 0
    for i in itertools.cycle(instructions):
        if pos.endswith("Z"):
            return counter
            break
        l, r = network[pos]
        if i == "L":
            pos = l
        elif i == "R":
            pos = r
        counter += 1


# Calculate the steps for each starting point
steps = []
for start in [a for a in network.keys() if a.endswith("A")]:
    steps.append(count_steps_to_z(start))
    print('{} → {}'.format(start, steps[-1]))

# Calculate the least common multiple of all steps to finde the number of steps needed
# for all paths to reach a node that ends on Z ;-)
print(steps)
print(math.lcm(*steps))
