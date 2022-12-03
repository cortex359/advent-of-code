with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

values = 0
for r in data:
	shared_item_list = [x for x in r[:int(len(r)/2)] for y in r[int(len(r)/2):] if x == y]
	shared_item_types = list(dict.fromkeys(shared_item_list))

	for x in [ord(v) for v in shared_item_types]:
		if x >= 97:
			prio = (x-32-64)
		else:
			prio = (x-64+26)

		values += prio

print("T1: ", values)

values = 0
for r in range(1, len(data), 3):
	shared_item_list = [x for x in data[r-1] for y in data[r+1] for z in data[r] if x == y and y == z]
	shared_item_types = list(dict.fromkeys(shared_item_list))

	for x in [ord(v) for v in shared_item_types]:
		if x >= 97:
			prio = (x-32-64)
		else:
			prio = (x-64+26)
		values += prio

print("T2: ", values)
