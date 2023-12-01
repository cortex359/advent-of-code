import re

with open("input") as file:
    data = [line.removesuffix("\n") for line in file]

number_words = {1: 'one',
                2: 'two',
                3: 'three',
                4: 'four',
                5: 'five',
                6: 'six',
                7: 'seven',
                8: 'eight',
                9: 'nine'}
summe = 0


def first_num(line):
    rank = []
    for d, word in number_words.items():
        if line.find(word) >= 0:
            rank.append((word, d, line.find(word)))

    rank = sorted(rank, key=lambda x: x[2])
    if len(rank) == 0:
        return re.sub(r'\D', '', line)[0]
    return re.sub(r'\D', '', re.sub(rank[0][0], str(rank[0][1]), line))[0]


def last_num(line):
    rank = []
    for d, word in number_words.items():
        if line.rfind(word) >= 0:
            rank.append((word, d, line.rfind(word)))

    rank = sorted(rank, key=lambda x: x[2], reverse=True)
    if len(rank) == 0:
        return re.sub(r'\D', '', line)[-1]
    return re.sub(r'\D', '', re.sub(r'(.*)' + rank[0][0], str(rank[0][1]), line))[-1]


for line in data:
    print('{} → {} + {}'.format(line, first_num(line), last_num(line)))
    summe += int(str(first_num(line)) + str(last_num(line)))

# 54518
print(summe)
