import re
import sys
from collections import deque

import numpy as np

file_path = sys.argv[1] if len(sys.argv) > 1 else 'input'

with open(file_path) as file:
    data: list = [line.removesuffix("\n") for line in file]


def display_cube(cube: np.ndarray, y_slice: int = 0):
    print(cube[:, y_slice, ::-1].T)


#   n x y z
#  20 0 0 0  #

#  32 0 0 1  ##
#  83 0 0 2  ###
#  25 0 0 3  ####
#   3 0 0 4  #####

# 140 0 1 0
# 359 0 2 0
# 181 0 3 0
#  10 0 4 0

# 162 1 0 0
# 315 2 0 0
# 153 3 0 0
#  14 4 0 0

def do_gravity(cube, cross_section, z):
    for dz in range(z, 0, -1):
        if np.multiply(cube[:, :, dz], cross_section).sum() > 0:
            return dz + 1
    return 1


def get_supporting_bricks(cube, cross_section, z) -> set[int]:
    return set(np.multiply(cube[:, :, z], cross_section).flatten()) - {0}


# Brick A: id, x, y, z, x, y, z
bricks: list[tuple[int, int, int, int, int, int, int]] = []
for line_number, line in enumerate(data):
    brick_id = line_number + 1
    a, b = line.split("~")
    bricks.append(tuple([brick_id, *map(int, a.split(",")), *map(int, b.split(","))]))

# sort by a_z position
bricks = sorted(bricks, key=lambda x: x[3], reverse=False)

max_x = max(bricks, key=lambda x: x[4])[4] + 1
max_y = max(bricks, key=lambda x: x[5])[5] + 1
max_z = max(bricks, key=lambda x: x[6])[6] + 1
print(f"max_x: {max_x}, max_y: {max_y}, max_z: {max_z}")

cube = np.zeros((max_x, max_y, max_z), dtype=int)

# resting_on_bricks:
#   maps every brick to a set of bricks directly below it
resting_on_bricks: dict[int, set[int]] = {}

for (brick_id, a_x, a_y, a_z, b_x, b_y, b_z) in bricks:
    assert b_x >= a_x and b_y >= a_y and b_z >= a_z
    brick_height = b_z - a_z

    # prepare bottom cross section view of falling brick
    cross_section = np.zeros((max_x, max_y), dtype=int)
    cross_section[a_x:b_x + 1, a_y:b_y + 1] = 1

    # do gravity until contact ^^
    z_fallen = do_gravity(cube, cross_section, a_z)

    # save whatever stopped the fall
    resting_on_bricks[brick_id] = get_supporting_bricks(cube, cross_section, z_fallen - 1)
    # print(f"Brick {brick_id} felt from height a_z={a_z} down to z={z_fallen}, hitting {resting_on_bricks[brick_id]}")
    cube[a_x:b_x + 1, a_y:b_y + 1, z_fallen:(z_fallen + brick_height + 1)] = brick_id

dependent_bricks: dict[int, set[int]] = {}
for brick, resting_on in resting_on_bricks.items():
    for r in resting_on:
        if r not in dependent_bricks:
            dependent_bricks[r] = set()
        dependent_bricks[r].add(brick)

disintegratable_bricks = set(range(1, len(bricks) + 1))
for brick in range(1, len(bricks) + 1):
    # when a brick is supported only by a single brick, that single brick can not be disintegrated
    if len(resting_on_bricks[brick]) < 2:
        disintegratable_bricks -= resting_on_bricks[brick]
    # print(f"Brick {brick} rests on {resting_on_bricks[brick]}")

### PART I
print(f"Safely disintegratable bricks: {disintegratable_bricks}")
print(f"In total there are {len(disintegratable_bricks)} safely disintegratable bricks. (Part I)")


### PART II
def do_chain_react(brick, dependend_bricks, resting_on_bricks):
    if dependend_bricks.get(brick) is None:
        return 0
    falling, queue = set(), deque(dependend_bricks[brick])
    while queue:
        b = queue.popleft()
        if b not in falling and len(resting_on_bricks[b] - falling - {brick}) < 1:
            falling.add(b)
            # look at all bricks dependent on brick b
            if b in dependend_bricks:
                queue.extend(dependend_bricks[b])

    return len(falling)


print(f"brick → resting on: {resting_on_bricks}")
print(f"brick → rested on (dependent): {dependent_bricks}")
falling = 0

# look at all bricks, that are not safely disintegratable (since
# the safely disintegratable ones won't cause other bricks to fall):
not_safely_disintegratable = set(range(1, len(bricks) + 1)) - disintegratable_bricks

for brick in not_safely_disintegratable:
    f = do_chain_react(brick, dependent_bricks, resting_on_bricks)
    falling += f

# 102770
print(f"For all {len(not_safely_disintegratable)} bricks that are not safely disintegratable, the sum of bricks that "
      f"could potentially fall, for each single brick we would disintegrating, is {falling}. (Part II)")
