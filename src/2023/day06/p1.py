import math
import re
from sympy import solve_univariate_inequality, Symbol, Interval
from time import perf_counter

# Part 1
# input
time     = [  56,     97,     78,     75]
distance = [ 546,   1927,   1131,   1139]

# example
#time     = [7,  15,   30]
#distance = [9,  40,  200]

# Part 2
# input
time     = 56977875
distance = 546192711311139

# example
#time     = 71530
#distance = 940200

#puzzle1 = 1
#for i in range(len(time)):
#    waysofrecord = 0
#
#    for j in range(time[i] + 1):
#        travel_distance = j * increase * (time[i] - j)
#        print('td{}, i{}'.format(travel_distance, j))
#        if travel_distance > distance[i]:
#            waysofrecord += 1
#    print(waysofrecord)
#    puzzle1 *= waysofrecord
#
#print(puzzle1)

t1_start = perf_counter()

x = Symbol('x')
solution = solve_univariate_inequality(x*(time-x) > distance, x).as_set()
print(math.floor(solution.right.evalf()) - math.floor(solution.left.evalf()))

t1_stop = perf_counter()
print("Elapsed time:", t1_stop, t1_start)
print("Elapsed time during the whole program in seconds:",
      t1_stop-t1_start)
