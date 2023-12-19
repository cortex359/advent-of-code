import re
import numpy as np
from collections import deque
from collections import defaultdict
import itertools

with open("input") as file:
    data: list = [line.removesuffix("\n") for line in file]


wof = True
workflows: dict[str, list] = {}
ratings = []
parts: list[dict[str, int]] = []
for l in data:
    if l == "":
        wof = False
        continue
    if wof:
        name = re.match(r'^[^{]+', l).group(0)
        rules = l[l.index('{')+1:-1].split(',')
        workflows[name] = rules
    else:
        quality_values: dict = {}
        for v in l[1:-1].split(','):
            quality_values[v.split('=')[0]] = int(v.split('=')[1])
        parts.append(quality_values)

def is_accepted(p, workflows):
    state = 'in'
    while state not in ('R', 'A'):
        print(f"{state} → ", end='')
        for r in workflows[state]:
            if r.count(':') == 0:
                state = r
                break

            # Check conditions
            condition, target_state = r.split(':')
            print(f"condition: {condition}, target_state: {target_state}")
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
    print()
    if state == 'R':
        return False
    if state == 'A':
        return True


x, m, a, s = (0, 0, 0, 0)
for p in parts:
    if is_accepted(p, workflows):
        print(f"Accepted: {p}")
        x, m, a, s = p['x']+x, p['m']+m, p['a']+a, p['s']+s


print(f"Summ for all: {x+m+a+s}")
