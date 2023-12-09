import re
from collections import deque


with open("input") as file:
    data: list = [line.removesuffix("\n") for line in file]

#############################################

def history_to_sequences(history):
    sequence = history.copy()
    sequences = [sequence]
    print(sequence)
    while sequence.count(0) < len(sequence):
        next_sequence = []
        for i in range(1, len(sequence)):
            delta = sequence[i] - sequence[i - 1]
            next_sequence.append(delta)
            print(delta, end=' ')
        sequence = next_sequence
        sequences.append(next_sequence)
        print()
    print()
    return sequences


extrapolation_sum = 0

for history in [list(map(int, l.split())) for l in data]:
    sequences = history_to_sequences(history)
    for i in range(len(sequences) - 2, -1, -1):
        adding = sequences[i][0] - sequences[i+1][0]
        #print('[{}] {} + {}'.format(i, sequences[i], adding))
        sequences[i].insert(0, adding)
    print(sequences[0][0])
    extrapolation_sum += sequences[0][0]

print("Part 1:", extrapolation_sum)