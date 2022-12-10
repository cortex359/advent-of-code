with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

# display | segments
#       1 |       cf |    c  f
#       7 |      acf |  a c  f
#       4 |     bcdf |   bcd f
#       2 |    acdeg |  a cde g
#       3 |    acdfg |  a cd fg
#       5 |    abdfg |  ab d fg
#       0 |   abcefg |  abc efg
#       6 |   abdefg |  ab defg
#       9 |   abcdfg |  abcd fg
#       8 |  abcdefg |  abcdefg

for line in data:
	patterns, output = line.split(" | ")
	figures = patterns.split()

	one:      set = set(c for c in [x for x in figures if len(x) == 2][0])
	seven:    set = set(c for c in [x for x in figures if len(x) == 3][0])
	four:     set = set(c for c in [x for x in figures if len(x) == 4][0])
	eight:    set = set(c for c in [x for x in figures if len(x) == 7][0])
	# 2, 3, 5
	length_5: list[set] = [y for z in [x for x in patterns.split() if len(x) == 5] for y in set(c for c in y)
	# 0, 6, 9
	length_6: list[set] = set(x for x in patterns.split() if len(x) == 6)

	print(one.intersection(seven, four))
