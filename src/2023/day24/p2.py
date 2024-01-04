import itertools
import random
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
    support_vector = np.array(list(map(int, p.split(","))), dtype=np.int64)
    # velocity in units per nanosecond (Richtungsvektor)
    direction_vector = np.array(list(map(int, v.split(","))), dtype=np.int64)

    trajectories.append((support_vector, direction_vector))


def positional_relationship(t1, t2):
    t1_support, t1_direction = t1
    t2_support, t2_direction = t2

    A = np.column_stack((t1_direction, t2_direction, (t1_support - t2_support)))
    # det(A) = 0, wenn Geraden identische, echt parallele oder schneidend sind == Geraden liegen in einer Ebene
    # det(A) != 0, wenn Geraden echt windschief sind
    return np.linalg.det(A)


# windschief?
#for a, b in itertools.combinations(trajectories, 2):
#    if -1e-10 < positional_relationship(a, b) < 1e-10:
#        print(f"Geraden {a} und {b} liegen in einer Ebene")

def is_linear_dependend(v1, v2):
    scaler = None
    for i in range(len(v1)):
        if v1[i] == 0 and v2[i] == 0:
            continue
        if v1[i] == 0 or v2[i] == 0:
            return False
        if scaler is None:
            scaler = v1[i] / v2[i]
        else:
            if scaler - 1e-5 < v1[i] / v2[i] < scaler + 1e-5:
                continue
            else:
                return False
    return True

# same velocity?
for a, b in itertools.combinations(trajectories, 2):
    if is_linear_dependend(a[0], b[0]):
        print(f"Geraden {a} und {b} haben gleiche Richtung:")



#for a, b, c in itertools.combinations(trajectories, 3):
#    matrix_A = np.column_stack((a[1], b[1], c[1]))
#    vector_b = a[0] + b[0] + c[0]
#
#    try:
#        vector_x = np.linalg.solve(matrix_A, vector_b)
#    except np.linalg.LinAlgError:
#        continue
#
#    crossing_a = a[0] + a[1] * vector_x[0]
#    crossing_b = b[0] + b[1] * vector_x[1]
#    crossing_c = c[0] + c[1] * vector_x[2]
#
#    if np.mod(crossing_a, 1).all() == 0 and np.mod(crossing_b, 1).all() == 0 and np.mod(crossing_c, 1).all() == 0 and np.mod(vector_x, 1).all() == 0:
#        if np.greater_equal(vector_x, 0).all():
#            if np.equal(vector_x, 0).any():
#                print(f"Found integer solution {vector_x} for {a}, {b} and {c} with crossing points {crossing_a}, {crossing_b} and {crossing_c}")

