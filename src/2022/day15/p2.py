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
        relevant_sbl.append(sbl)

no_beacon: set = set()

# -802_144, 3_980_013
# size: 4_782_164
# for x in range(-1_802_144, 4_000_000):

# for rsbl in relevant_sbl:
#     sx, sy, bx, by, mrad = rsbl
#     mrad -= abs(sy - y)
#     for x in range(sx - mrad, sx + mrad + 1):
#         if (x, y) == (bx, by):
#             continue
#         no_beacon.add(f"{x}")


may_beacon: set = set()

for a, asbl in enumerate(all_sbl):
    sx, sy, bx, by, mrad = asbl
    for b, bsbl in enumerate(all_sbl):
        if asbl == bsbl:
            continue
        s2x, s2y, b2x, b2y, m2rad = bsbl
        sensor_distance = abs(s2x - sx) + abs(s2y - sy)

        middle_dist = abs(sensor_distance - (mrad + m2rad))
        if middle_dist == 2:
            print(middle_dist, a, b)
            d_x = abs(s2x - sx)
            d_y = abs(s2y - sy)

# middle_dist == 2:
# 6 28
# 23 32

for rsbl in all_sbl[6], all_sbl[28], all_sbl[23], all_sbl[32]:
    sx, sy, bx, by, mrad = rsbl
    for y in range(2935106 - 2, 3676457 + 4):
        mrad -= abs(sy - y)
        for x in range(2650714 - 2, 3236266 + 4):
            if (x, y) == (bx, by):
                continue
            may_beacon.add(f"{x}:{y}")



#all_sbl[23] bis all_sbl[32]

#print(all_sbl[6][0:2])
#print(all_sbl[28][0:2])
#print(all_sbl[23][0:2])
#print(all_sbl[32][0:2])

# x
# 3236266-3171811 =  64455
# 2806673-2650714 = 155959
#                d1 369593
#                d1 684789
# y
# 3676457 - 3674470 = 1987
# 3051666 - 2935106 = 116560

## Part II
# 0 < 4000000

for mb in may_beacon:
    sig_x, sig_y = map(int, mb.split(":"))
    tuning_freq = sig_x * 4000000 + sig_y
    print(tuning_freq)

## Part I
# to low 4406724
#        5367037
# 11914583249288
#print(len(no_beacon))
