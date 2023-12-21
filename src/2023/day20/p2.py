import math
import re
import numpy as np
from collections import deque
from collections import defaultdict
import itertools

with open("input") as file:
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
    last_mods: dict[str, bool] = {'ls': 0, 'qq': 0, 'bg': 0, 'sj': 0}
    queue = deque(list(zip(broadcaster, ['low'] * len(broadcaster))))
    low_pulses = 1
    high_pulses = 0
    while queue:
        module, signal = queue.popleft()
        if module == 'rx' and signal == 'low':
            return -1, -1

        # ['dl', 'hf', 'lq', 'hb']
        if module in last_mods.keys():
            last_mods[module] = signal == 'high'

        #print(f" -{signal} → {module}")
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
            if module == 'output' or module == 'rx':
                continue
            print(f"module: {module}, signal: {signal}")
            print("Error")

    return conj_inputs['kz']
    #return dict(**conj_inputs['hb'], ** conj_inputs['lq'], ** conj_inputs['hf'], ** conj_inputs['dl'])

# dl → 4076987239710
# sv: 2
# jp: 3
# sh: 15
# pf: 63
# gv: 127
# tj: 511
# zs: 1023
# nh: 2047
#intervalls: dict[str, int] = {'sv': 0, 'pf': 0, 'jp': 0, 'gv': 0, 'zs': 0, 'tj': 0, 'nh': 0, 'sh': 0}

# hb → 6144
# bm: 2
# mr: 3
# pd: 4
# xg: 8
# zq: 64
# vk: 256
# fx: 512
# fl: 1024
# rj: 2048
#intervalls: dict[str, int] = {'mr': 0, 'pd': 0, 'rj': 0, 'bm': 0, 'xg': 0, 'zq': 0, 'fl': 0, 'vk': 0, 'fx': 0}


# lq → 6144
# xn: 2
# xr: 3
# lr: 8
# jj: 16
# rd: 128
# sx: 512
# fn: 1024
# zr: 2048
# intervalls: dict[str, int] = {'jj': 0, 'sx': 0, 'fn': 0, 'lr': 0, 'xn': 0, 'zr': 0, 'xr': 0, 'rd': 0}

# hf → 6144
# rg: 3
# fb: 2
# vg: 32
# np: 128
# cl: 256
# gj: 512
# dv: 1024
# xl: 2048
# intervalls: dict[str, int] = {'xl': 0, 'vg': 0, 'dv': 0, 'fb': 0, 'np': 0, 'cl': 0, 'gj': 0, 'rg': 0}

#offset: dict[str, int] = {'mr': 0, 'pd': 0, 'rj': 0, 'bm': 0, 'xg': 0, 'zq': 0, 'fl': 0, 'vk': 0, 'fx': 0, 'jj': 0, 'sx': 0, 'fn': 0, 'lr': 0, 'xn': 0, 'zr': 0, 'xr': 0, 'rd': 0, 'xl': 0, 'vg': 0, 'dv': 0, 'fb': 0, 'np': 0, 'cl': 0, 'gj': 0, 'rg': 0, 'sv': 0, 'pf': 0, 'jp': 0, 'gv': 0, 'zs': 0, 'tj': 0, 'nh': 0, 'sh': 0}
#intervalls: dict[str, int] = {'mr': 0, 'pd': 0, 'rj': 0, 'bm': 0, 'xg': 0, 'zq': 0, 'fl': 0, 'vk': 0, 'fx': 0, 'jj': 0, 'sx': 0, 'fn': 0, 'lr': 0, 'xn': 0, 'zr': 0, 'xr': 0, 'rd': 0, 'xl': 0, 'vg': 0, 'dv': 0, 'fb': 0, 'np': 0, 'cl': 0, 'gj': 0, 'rg': 0, 'sv': 0, 'pf': 0, 'jp': 0, 'gv': 0, 'zs': 0, 'tj': 0, 'nh': 0, 'sh': 0}

#offset: dict[str, int] = {'ls': 0, 'qq': 0, 'bg': 0, 'sj': 0}
#intervalls: dict[str, int] = {'dl': 0, 'hf': 0, 'lq': 0, 'hb': 0}

intervalls: dict[str, int] = {'ls': 0, 'qq': 0, 'bg': 0, 'sj': 0}
#prev_state: dict[str, bool] = button_push(broadcaster, flip_modules, conj_modules)

i = 0
dl_state: dict[str, int]

while True:
    i += 1
    dl_state = button_push(broadcaster, flip_modules, conj_modules)
    print(dl_state)
    for k, v in dl_state.items():
        if v and intervalls[k] == 0:
            intervalls[k] = i
            print(f"New intervall for {k}: {i}")
    if all(intervalls.values()) != 0:
        break
    if i % 100 == 0:
        pass
        #print(i)

print(intervalls)
# 4076987239710 to low
# 4174834933463040 too high
# 222718819437131 it is
print(math.lcm(*intervalls.values()))
