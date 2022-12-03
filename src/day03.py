from utils.api import get_input

input_str = get_input(3)

values = 0
for r in input_str:
    shared_item_list = [x for x in r[:int(len(r)/2)] for y in r[int(len(r)/2):] if x == y]
    shared_item_types = list(dict.fromkeys(shared_item_list))

    for x in [ord(v) for v in shared_item_types]:
        if x >= 97:
            prio = (x-32-64)
        else:
            prio = (x-64+26)

        values += prio

print("T1: ", values)

values = 0
for r in range(1, len(input_str), 3):
    shared_item_list = [x for x in input_str[r-1] for y in input_str[r+1] for z in input_str[r] if x == y and y == z]
    shared_item_types = list(dict.fromkeys(shared_item_list))

    for x in [ord(v) for v in shared_item_types]:
        if x >= 97:
            prio = (x-32-64)
        else:
            prio = (x-64+26)
        values += prio

print(values)
