import re
import numpy as np
from collections import deque
from collections import defaultdict
import itertools

# d = defaultdict(int)  # Default to int (0)

with open("input") as file:
    data: list = [line.removesuffix("\n") for line in file]

# Parsing Stuff
# -------------

# Part 1:
points =  0
for line in data:
    id = int(line.removeprefix("Card ").split(":")[0])
    winning_numbers = line.split("|")[0].split(":")[1].strip().split(" ")
    my_numbers = line.split("|")[1].strip().split(" ")
    #print(id, winning_numbers, my_numbers)

    winning_numbers = list(filter(None, winning_numbers))
    my_numbers = list(filter(None, my_numbers))
    my_winning = set(winning_numbers).intersection(set(my_numbers))
    if len(my_winning) > 0:
        points += 2 ** (len(my_winning) - 1)

print(points)

# Part 2:
point_cards = {}
doublings = [1 for i in data]
toal_points = 0

# Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53

# you win copies of the scratchcards below the winning card equal to the number of matches
for line in data:
    id = int(line.removeprefix("Card ").split(":")[0])
    winning_numbers = line.split("|")[0].split(":")[1].strip().split(" ")
    my_numbers = line.split("|")[1].strip().split(" ")
    #print(id, winning_numbers, my_numbers)

    winning_numbers = list(filter(None, winning_numbers))
    my_numbers = list(filter(None, my_numbers))
    my_winning = set(winning_numbers).intersection(set(my_numbers))
    for wi in range(id, id + len(my_winning)):
        doublings[wi] += doublings[id - 1]
    toal_points += doublings[id-1]

# 10378710
print(toal_points)

