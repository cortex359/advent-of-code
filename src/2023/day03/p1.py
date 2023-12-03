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

summation = 0
for i in range(len(data)):
    for findex, num in [(m.start(0), m.group()) for m in re.finditer(r'[0-9]+', data[i])]:
        adj = False
        if findex != 0:
            if data[i][findex - 1] != ".":
                adj = True
                print('{} → left'.format(num))
        if findex + len(num) != len(data[i]):
            if data[i][findex + len(num)] != ".":
                adj = True
                print('{} → right'.format(num))
        if i != 0:
            if findex == 0:
                start = 0
            else:
                start = findex - 1
            if findex + len(num) >= len(data[i - 1]):
                end = len(data[i - 1]) - 1
            else:
                end = findex + len(num) + 1

            if data[i - 1][start:end].replace(r'\d', '.').count(".") != len(data[i - 1][start:end]):
                adj = True
                print('{} → adj top or top diagonal'.format(num))
        if i != len(data) - 1:
            if findex == 0:
                start = 0
            else:
                start = findex - 1
            if findex + len(num) >= len(data[i + 1]):
                end = len(data[i + 1]) - 1
            else:
                end = findex + len(num) + 1
            print('bottom {}'.format(data[i + 1][start:end].replace(r'\d', '.')))
            if data[i + 1][start:end].replace(r'\d', '.').count(".") != len(data[i + 1][start:end]):
                adj = True
                print('{} → adj bottom or bottom diagonal'.format(num))

        if not adj:
            print('{} → not adj'.format(num))
        if adj:
            summation += int(num)

# → 539637
print(summation)
