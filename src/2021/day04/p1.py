import numpy as np

with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

draw = list(map(int, data[0].split(",")))

data.append("")

rows = []
boards = []
a = []
b = []
c = []
d = []
e = []
for line in data[2:]:
	if line == "":
		# next board
		rows.append(a)
		rows.append(b)
		rows.append(c)
		rows.append(d)
		rows.append(e)
		boards.append(rows)
		rows = []
		a = []
		b = []
		c = []
		d = []
		e = []
	else:
		row = [int(line[0:2].strip()),
			int(line[3:5].strip()),
			int(line[6:8].strip()),
			int(line[9:11].strip()),
			int(line[12:14].strip())
		]
		rows.append(row)
		a.append(int(line[0:2].strip()))
		b.append(int(line[3:5].strip()))
		c.append(int(line[6:8].strip()))
		d.append(int(line[9:11].strip()))
		e.append(int(line[12:14].strip()))


def bingo_after(board):
	for drawing in range(5, len(draw)):
		for r in board:
			if len([x for x in r if x in draw[:drawing]]) == 5:
				# print("Bingo at ", draw[drawing-1], " after ", (drawing-1), "draws.")
				return drawing-1

i = 0
best_board_stats = 9999
best_board = -1
for b in boards:
	# print("Board Nr.: ", i)
	stats = bingo_after(b)
	if stats < best_board_stats:
		best_board = i
		best_board_stats = stats
	i += 1

print("Best board is board no. ", best_board, " winning after draw no. ", best_board_stats)

sum_of_all_unmarked_numbers = sum([x for x in np.array(boards[best_board][:5]).flat if x not in draw[:best_board_stats+1]])
print("Score: ", sum_of_all_unmarked_numbers * draw[best_board_stats])

### PART 2 ###

i = 0
worst_board_stats = 0
worst_board = -1
for b in boards:
	# print("Board Nr.: ", i)
	stats = bingo_after(b)
	if stats > worst_board_stats:
		worst_board = i
		worst_board_stats = stats
	i += 1

print("Worst board is board no. ", worst_board, " winning not before draw no. ", worst_board_stats)

sum_of_all_unmarked_numbers = sum([x for x in np.array(boards[worst_board][:5]).flat if x not in draw[:worst_board_stats+1]])
print("Score: ", sum_of_all_unmarked_numbers * draw[worst_board_stats])
