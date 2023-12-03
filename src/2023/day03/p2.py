import re

with open("input") as file:
    data = [line.removesuffix("\n") for line in file]

data_alt = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "+5....755.",
    "...$......",
    ".664.598.."
]


def get_number_from_segment(line, index):
    while line[index].isdigit():
        index -= 1
    index += 1
    end = index
    while end < len(line) and line[end].isdigit():
        end += 1

    return line[index:end]


# 4.5
# .↑.
# wobei ↑ auf Index zeigt und 4.5 die Zeile ist
def check_segment(line, index, length):
    start = 0 if index == 0 else index - 1
    end = len(line) - 1 if index + length >= len(line) else index + length + 1
    adj = []
    i = start
    while i < end:
        if line[i] != ".":
            number = get_number_from_segment(line, i)
            adj.append(number) if number != "" else None
        i += 1
    return list(set(adj))


def in_bounds(i):
    return 0 <= i < len(data)


## Part 2
gear_ratios = 0
for i in range(len(data)):
    for findex in [(m.start(0)) for m in re.finditer(r'\*', data[i])]:
        adj: list = check_segment(data[i], findex, 1)
        if in_bounds(i - 1):
            adj += check_segment(data[i - 1], findex, 1)
        if in_bounds(i + 1):
            adj += check_segment(data[i + 1], findex, 1)
        # print(adj)

        if len(adj) == 2:
            gear_ratios += int(adj[0]) * int(adj[1])

# → 82818007
print(gear_ratios)
