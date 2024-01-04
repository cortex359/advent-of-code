import itertools
import sys
import numpy as np
import scipy

file_path = sys.argv[1] if len(sys.argv) > 1 else 'input'

with open(file_path) as file:
    data: list = [line.removesuffix("\n") for line in file]

# test area
test_min, test_max = (200000000000000, 400000000000000) if file_path == 'input' else (7, 27)

# Parse
trajectories: list[tuple] = []
for l in data:
    p, v = l.split("@")
    # position at time 0 (Stützvektor)
    px, py, pz = map(int, p.split(","))
    # velocity in units per nanosecond (Richtungsvektor)
    vx, vy, vz = map(int, v.split(","))

    trajectories.append((px, py, pz, vx, vy, vz))


# check
def check_intersection(eq1, eq2):
    px_1, py_1, pz_1, vx_1, vy_1, vz_1 = eq1
    px_2, py_2, pz_2, vx_2, vy_2, vz_2 = eq2
    # b = np.array(px_1 - px_2, py_1 - py_2, pz_1 - pz_2)
    # A = np.array([[vx_2, vx_1], [vy_2, vy_1]])

    b = np.array([px_1 - px_2, py_1 - py_2])
    A = np.array([[vx_2, vx_1], [vy_2, vy_1]])

    try:
        x = scipy.linalg.solve(A, b)
    except scipy.linalg.LinAlgError:
        return False

    # x is vector (beta, -alpha)

    # check if trajectory is in the past
    if x[0] < 0 or x[1] > 0:
        return False

    meeting_point = (px_1 + vx_1 * -x[1], py_1 + vy_1 * -x[1])
    # print(f"meeting at x|y : {px_1 + vx_1 * -x[1]}|{py_1 + vy_1 * -x[1]} == {px_2 + vx_2 * x[0]}|{py_2 + vy_2 * x[0]}")

    return meeting_point


def inside_test_area(pos):
    # check if meeting point is in test area
    return test_min <= pos[0] <= test_max and test_min <= pos[1] <= test_max


count_intersections = 0
for a, b in itertools.combinations(trajectories, 2):
    intersection = check_intersection(a, b)
    if intersection and inside_test_area(intersection):
        print(f"intersection at {intersection}")
        count_intersections += 1

print(count_intersections)
