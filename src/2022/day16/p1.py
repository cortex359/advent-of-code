import re
import sys
from collections import deque
import itertools
import time as timelib

from copy import deepcopy

if "-i" in sys.argv:
	target = "input"
else:
	target = "example"

with open(target) as file:
	data = [line.removesuffix("\n") for line in file]
print(f"Loaded {target} file with {len(data)} lines.\n")

# Valve VO has flow rate=6; tunnels lead to valves KM, RF, HS, LJ, IA
# 1 min to open + 1 min to change pos


class Valve:
	def __init__(self, name, flow_rate, adj):
		self.name = name
		self.flow_rate = flow_rate
		self.adj = adj
		self.time = 0


valves: dict[str, Valve] = {}

for v in data:
	if v.startswith("Valve "):
		print(v)
		name = v.split(" ")[1]
		flow_rate = int(re.findall(r"rate=(\d+)", v)[0])
		adj = re.findall(r"to valves? (.*)$", v)[0].split(", ")
		valves[name] = Valve(name, flow_rate, adj)
		print(name, flow_rate, adj)


queue = deque([valves['AA']])

while queue:
	current = queue.popleft()
	print(current.name)
	for adj in current.adj:
		queue.append(valves[adj])
		print(adj)
	print()



# >>>>>>-------<<<<<<
#       PART  I
# >>>>>>-------<<<<<<
# >>> 1737

# >>>>>>-------<<<<<<
#       PART II
# >>>>>>-------<<<<<<
# >>> 2216
