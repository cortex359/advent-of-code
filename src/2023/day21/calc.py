import numpy as np
from numpy.polynomial import Polynomial


plot_numbers = [3814, 33952, 94138, 184372, 304654, 454984, 635362, 845788, 1086262, 1356784, 1657354]
steps = [65, 196, 327, 458, 589, 720, 851, 982, 1113, 1244, 1375]

for i in range(1, 11):
    delta_plot = plot_numbers[i] - plot_numbers[i - 1]
    print(f"{i} {plot_numbers[i] / steps[i]} {delta_plot} {(delta_plot - i) / i}")

delta = 30063
estimation = 0
for i in range(1, 202300 + 1):
    estimation += delta * i

print(f"Very rough estimation to get the order of magnitude\n{estimation}")

def identified_sequence(n):
    return 2 * (7512 * ((n+1) ** 2) - 7467 * (n+1) + 1862)

print(f"Prediction for 12: {identified_sequence(12)}")
print(f"Prediction for 202300:\n{identified_sequence(202300)}")

print(15024*202301**2 - 14934*202301 + 3724)

def fit_polynomial(y):
    from numpy.polynomial import Polynomial
    return Polynomial.fit(list(range(len(y))), y, 2)


plot_numbers = np.array([3814, 33952, 94138], dtype=np.int_)
X = np.array([0, 1, 2], dtype=np.int_)
A = np.array([X**i for i in range(X.shape[0])]).T
poly = Polynomial(np.linalg.solve(A, plot_numbers))
print(poly(202300), f"lin solve with {poly}")
