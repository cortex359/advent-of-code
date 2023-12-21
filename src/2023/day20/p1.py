import re
import numpy as np
from collections import deque
from collections import defaultdict
import itertools

with open("example3") as file:
    data: list = [line.removesuffix("\n") for line in file]

flip_modules: dict[list] = {}
conj_modules: dict = {}
conj_inputs: dict = {}
broadcaster: list = []
for l in data:
    a, b = l.split(" -> ")
    if a != "broadcaster":
        module, name = a[0], a[1:]
        destinations = b.split(", ")
        #print(module, name, destinations)
        # flip_modules -> state, [a, b, c, d]
        if module == "%":
            flip_modules[name] = [False, destinations]
        elif module == "&":
        # conj_modules[name] -> [(a, state), (b, state)]
            #conj_modules[name] = (list(zip(connected_modules, [False] * len(connected_modules))))
            conj_modules[name] = destinations
            #print(conj_modules[name])
    else:
        broadcaster = b.split(", ")

for key in conj_modules.keys():
    conj_inputs[key]: dict = {}

for name, fm in flip_modules.items():
    state, destinations = fm
    for d in destinations:
        if d in conj_modules:
            conj_inputs[d][name] = False

for name, cm in conj_modules.items():
    for d in cm:
        if d in conj_modules:
            conj_inputs[d][name] = False

#print(conj_inputs)

# flip_modules[name] -> state, [a, b, c, d]
# conj_modules[name] -> [a, b, c, d]
# conj_inputs[name] -> {a: False, b: False}
def button_push(broadcaster: list, flip_modules: dict, conj_modules: dict):
    queue = deque(list(zip(broadcaster, ['low'] * len(broadcaster))))
    low_pulses = 1 # len(broadcaster)
    high_pulses = 0

    while queue:
        module, signal = queue.popleft()
        print(f" -{signal} → {module}")
        if signal == 'low':
            low_pulses += 1
        elif signal == 'high':
            high_pulses += 1
        else:
            print("Error")
            return -1, -1

        # Flip %
        if module in flip_modules:
            if signal == 'low':
                flip_modules[module][0] = not flip_modules[module][0]
                for m in flip_modules[module][1]:
                    queue.append((m, 'high' if flip_modules[module][0] else 'low'))
                    # update memory of conjunction modules
                    if m in conj_modules:
                        conj_inputs[m][module] = flip_modules[module][0]

    # Conjunction &
        elif module in conj_modules:
            all_true = True
            for s in conj_inputs[module].values():
                all_true = s and all_true
            for m in conj_modules[module]:
                queue.append((m, 'low' if all_true else 'high'))
                # update memory of conjunction modules
                if m in conj_modules:
                    conj_inputs[m][module] = not all_true
        else:
            if module == 'output':
                continue
            print(f"module: {module}, signal: {signal}")
            print("Error")

    return low_pulses, high_pulses

total_low_pulses, total_high_pulses = 0, 0
for i in range(2):
    low_pulses, high_pulses = button_push(broadcaster, flip_modules, conj_modules)
    total_low_pulses += low_pulses
    total_high_pulses += high_pulses

print(f"Total low pulses: {total_low_pulses}")
print(f"Total high pulses: {total_high_pulses}")
print(f"Product: {total_low_pulses * total_high_pulses}")
