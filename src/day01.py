from utils.api import get_input

input_str = get_input(1)

elves = []
calories = 0

for l in input_str:
    if l == '':
        elves.append(calories)
        calories = 0
    else:
        calories += int(l)

elves.sort(reverse=True)

print(elves[0])

print(sum(elves[:3]))