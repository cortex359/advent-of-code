with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

cols: list[list[int]] = [[]] * 99
rows: list[list[int]] = []


def visible(r, c, height):
	# print("Check 1")
	left = [t for t in rows[r][:c] if t >= height]

	# print("Check 2")
	rev = rows[r][c + 1:]
	rev.reverse()
	right = [t for t in rev if t >= height]

	# print("Check 3")
	top = [t for t in cols[c][:r] if t >= height]

	# print("Check 4")
	rev = cols[c][r + 1:]
	rev.reverse()
	down = [t for t in rev if t >= height]

	# print(f"Checking {r}:{c}")
	# print(f"left: {left}\tright: {right}\ttop: {top}\tdown: {down}\n")

	return len(left) == 0 or len(right) == 0 or len(top) == 0 or len(down) == 0


def scenic_score(r, c, height):
	viewing_distance: list[int] = [0] * 4
	rev = rows[r][:c]
	rev.reverse()
	for t in rev:
		viewing_distance[0] += 1
		if t >= height:
			break

	for t in rows[r][c + 1:]:
		viewing_distance[1] += 1
		if t >= height:
			break

	rev = cols[c][:r]
	rev.reverse()
	for t in rev:
		viewing_distance[2] += 1
		if t >= height:
			break

	for t in cols[c][r + 1:]:
		viewing_distance[3] += 1
		if t >= height:
			break

	# print(f"Checking {r}:{c}: {viewing_distance}")
	return viewing_distance[0] * viewing_distance[1] * viewing_distance[2] * viewing_distance[3]


# get height map as list of rows and list of cols
for r, row in enumerate(data):
	rows.append([int(e) for e in row])

cols = [list(x) for x in list(zip(*rows))]

# count visible trees and calculate scenic scores for every tree
visible_trees = 0
scenic_scores: list[int] = []
scenic_places: dict = {}

for r, row in enumerate(data):
	for c, col in enumerate(row):
		if visible(r, c, int(col)):
			visible_trees += 1
		scenic_places[f"{r}:{c}"] = scenic_score(r, c, int(col))

print(f"There are {visible_trees:,} visible trees from outside the forest.")

ideal_spot = sorted(scenic_places.items(), key=lambda item: item[1], reverse=True)[0]

print(f"The tree at x:y = {ideal_spot[0]} with the highest scenic score of {ideal_spot[1]:,} "
      f"is the ideal spot for a tree house.")
