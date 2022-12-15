import re
import numpy as np

with open("input") as file:
    data = [line.removesuffix("\n") for line in file]

# -802_154 < x < 3_980_003
#   35_725 < y < 4_282_497

sbl: list = []
# Test line
y = 2_000_000
# y=10

all_sbl: list = []
relevant_sbl: list = []

# Sensor at x=12, y=14: closest beacon is at x=10, y=16
for line in data:
    # => im Rechteck sind keine Becons, ausßer 1 an der Stelle bx, by
    sx, sy, bx, by = map(int, re.findall("[xy]=([0-9-]+)", line))

    mrad = abs(by - sy) + abs(bx - sx)
    sbl = (sx, sy, bx, by, mrad)

    all_sbl.append(sbl)
    if y in range(sy - mrad, sy + mrad):
        print(sbl)
        relevant_sbl.append(sbl)

no_beacon: set = set()

# -802_144, 3_980_013
# size: 4_782_164
# for x in range(-1_802_144, 4_000_000):
for rsbl in relevant_sbl:
    sx, sy, bx, by, mrad = rsbl

    mrad -= abs(sy - y)

    for x in range(sx - mrad, sx + mrad + 1):
        if (x, y) == (bx, by):
            continue
        no_beacon.add(f"{x}")

# to low 4406724
#        5367037
# 11914583249288
print(len(no_beacon))
