import re
import numpy as np
from collections import deque
from collections import defaultdict
import itertools

with open("input") as file:
    data: list = [line.removesuffix("\n") for line in file]


workflows: dict[str, list] = {}
for l in data:
    if l == "":
        break
    name = re.match(r'^[^{]+', l).group(0)
    rules = l[l.index('{')+1:-1].split(',')
    workflows[name] = rules

def is_accepted(p, workflows):
    state = 'in'
    while state not in ('R', 'A'):
        #print(f"{state} → ", end='')
        for r in workflows[state]:
            if r.count(':') == 0:
                state = r
                break

            # Check conditions
            condition, target_state = r.split(':')
            #print(f"condition: {condition}, target_state: {target_state}")
            if condition.count('<') == 1:
                var, op = condition.split('<')
                if p[var] < int(op):
                    state = target_state
                    break
            elif condition.find('>'):
                var, op = condition.split('>')
                if p[var] > int(op):
                    state = target_state
                    break
            else:
                print(f"Problem with condition: {condition} and target_state: {target_state}")
    if state == 'R':
        return False
    if state == 'A':
        return True


# slice ranges
ranges: dict[str, set[int]] = {
    'x': {1,  4001},
    'm': {1,  4001},
    'a': {1,  4001},
    's': {1,  4001}
}

for name, workflow in workflows.items():
    for r in workflow:
        if r.count(':') == 0:
            state = r
            break

        # Check conditions
        condition: str
        condition, target_state = r.split(':')
        if condition.count('<') == 1:
            var, op = condition.split('<')
            ranges[var].add(int(op))
        elif condition.count('>') == 1:
            var, op = condition.split('>')
            ranges[var].add(int(op) + 1)


#p = {'x': x, 'm': m, 'a': a, 's': s}
#if is_accepted(p, workflows):
#    accepted_combinations += 1

# Ohne slicing:
# combinations = 256000000000000 (4000 ** 4)
# mit slicing:
# combinations = 5049336050
combinations = 1
accepted_combinations = 0
not_accepted_combinations = 0

# Teste die Grenzen der geteilten Intervalle
last_p = None

x_sorted = sorted(list(ranges['x']))
m_sorted = sorted(list(ranges['m']))
a_sorted = sorted(list(ranges['a']))
s_sorted = sorted(list(ranges['s']))

progress_counter = 0
for x_i in range(1, len(x_sorted)):
    x = x_sorted[x_i]
    x_last = x_sorted[x_i - 1]
    x_size = x - x_last

    for m_i in range(1, len(m_sorted)):
        m = m_sorted[m_i]
        m_last = m_sorted[m_i - 1]
        m_size = m - m_last

        for a_i in range(1, len(a_sorted)):
            a = a_sorted[a_i]
            a_last = a_sorted[a_i - 1]
            a_size = a - a_last

            for s_i in range(1, len(s_sorted)):
                progress_counter += 1
                s = s_sorted[s_i]
                s_last = s_sorted[s_i - 1]
                s_size = s - s_last

                p = {'x': x_last, 'm': m_last, 'a': a_last, 's': s_last}
                if is_accepted(p, workflows):
                    accepted_in_range = x_size * m_size * a_size * s_size
                    #print(f"x: {x_last}→{x}, {m_last}→{m}, {a_last}→{a}, {s_last}→{s}")
                    #print(f"{p}: accepted_in_range: {accepted_in_range}")
                    accepted_combinations += accepted_in_range
                else:
                    not_accepted_in_range = x_size * m_size * a_size * s_size
                    not_accepted_combinations += not_accepted_in_range
        print(f"Progress: {progress_counter / 50493360.50} %, total {progress_counter} checks")

#print("167409079868000 (expected)")
print(f"{accepted_combinations} (accepted_combinations) ")

print(f"Expected total:\n {4000 ** 4}")
print(f"accepted + not accepted = total: {accepted_combinations} + {not_accepted_combinations} =\n {accepted_combinations + not_accepted_combinations}")
print(f"Problematic: {1 - ((accepted_combinations + not_accepted_combinations) / 4000 ** 4)}")