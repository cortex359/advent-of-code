import itertools

with open("input") as file:
    data: list = [line.removesuffix("\n") for line in file]

instructions = list(data[0].strip())
network: dict = {}

for line in [l for l in data[1:] if l != ""]:
    line = line.replace("(", "").replace(")", "")
    node = line.split(" = ")[0]
    l, r = line.split(" = ")[1].split(", ")
    network[node] = (l, r)

pos = "AAA"
counter = 0
for i in itertools.cycle(instructions):
    print(i, pos)
    if pos == "ZZZ":
        print(counter)
        break
    l, r = network[pos]
    if i == "L":
        pos = l
    elif i == "R":
        pos = r
    counter += 1
