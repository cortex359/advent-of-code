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

# default_figs: dict = {
# 	0 :  abcefg
# 	1 :      cf
# 	2 :   acdeg
# 	3 :   acdfg
# 	4 :    bcdf
# 	5 :   abdfg
# 	6 :  abdefg
# 	7 :     acf
# 	8 : abcdefg
# 	9 :  abcdfg
# }

data = [ "abcefg cf acdeg acdfg bcdf abdfg abdefg acf abcdefg abcdfg | ... " ]

for line in data:
	patterns, output = line.split(" | ")
	figures = patterns.split()

	one:      set = set(c for c in [x for x in figures if len(x) == 2][0])
	seven:    set = set(c for c in [x for x in figures if len(x) == 3][0])
	four:     set = set(c for c in [x for x in figures if len(x) == 4][0])
	eight:    set = set(c for c in [x for x in figures if len(x) == 7][0])
	# 2, 3, 5
	length_5: list[set] = []
	for c in [x for x in figures if len(x) == 5]:
		length_5.append(set(y for y in c))
	# 0, 6, 9
	length_6: list[set] = []
	for c in [x for x in figures if len(x) == 6]:
		length_6.append(set(y for y in c))

	a: str = [x for x in seven.difference(one)][0]

	cde: set = set((
		eight.difference(length_6[0]).pop(),
		eight.difference(length_6[1]).pop(),
		eight.difference(length_6[2]).pop()
	))

	print(one.intersection(seven, four))
