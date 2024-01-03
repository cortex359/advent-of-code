import sys
import re
import numpy as np
from collections import deque
from collections import defaultdict
import itertools

file_path = sys.argv[1] if len(sys.argv) > 1 else 'input'

with open(file_path) as file:
    data: list = [line.removesuffix("\n") for line in file]

for l in data:
    p, v = l.split("@")
    px, py, pz = p.split(",")
    vx, vy, vz = v.split(",")

    print(px, py, pz, vx, vy, vz)

