import re

with open("input") as file:
    data = [line.removesuffix("\n") for line in file]


def test_3(line):
    for n in ("ab", "cd", "pq", "xy"):
        if line.find(n) != -1:
            return False
    return True


def test_1(line):
    return (line.count("a") + line.count("e")
            + line.count("i") + line.count("o")
            + line.count("u") >= 3)

def test_2(line):
	for i in range(len(line) - 1):
		if line[i] == line[i + 1]:
			return True
	return False

nice_strings = 0
for line in data:
	if test_1(line) and test_2(line) and test_3(line):
		nice_strings += 1

print(nice_strings)

def test_4(line):
	return len(re.findall(r'(..).*\1', line)) > 0

def test_5(line):
	return len(re.findall(r'(.).\1', line)) > 0

nice2_strings = 0
for line in data:
	if test_4(line) and test_5(line):
		nice2_strings += 1

print(nice2_strings)
