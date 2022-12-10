with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

# display | segments
#       1 |       cf
#       7 |      acf
#       4 |     bcdf
#       2 |    acdeg
#       3 |    acdfg
#       5 |    abdfg
#       0 |   abcefg
#       6 |   abdefg
#       9 |   abcdfg
#       8 |  abcdefg

for line in data:
	patterns, output = line.split(" | ")
	[x for x in patters.split() if len(x) <= 4]