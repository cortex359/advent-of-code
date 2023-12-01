import re

with open("input") as file:
    data = [line.removesuffix("\n") for line in file]

summe = 0

def first_num(line):
    d = 1
    rank = []

    for word in ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'):
        if line.find(word) >= 0:
            rank.append((word, d, line.find(word)))
        d += 1

    rank = sorted(rank, key=lambda x: x[2], reverse=False)
    if len(rank) == 0:
        return re.sub(r'\D', '', line)[0]
    return re.sub(r'\D', '', re.sub(rank[0][0], str(rank[0][1]), line))[0]


def last_num(line):
    d = 1
    rank = []

    for word in ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'):
        if line.rfind(word) >= 0:
            rank.append((word, d, line.rfind(word)))
        d += 1

    rank = sorted(rank, key=lambda x: x[2], reverse=True)
    if len(rank) == 0:
        return re.sub(r'\D', '', line)[-1]
    return re.sub(r'\D', '', re.sub(r'(.*)'+rank[0][0], str(rank[0][1]), line))[-1]


for line in data:
    print('{} → {} + {}'.format(line, first_num(line), last_num(line)))
    summe += int(str(first_num(line)) + str(last_num(line)))

print(summe)
