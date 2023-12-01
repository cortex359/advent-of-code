with open("input") as file:
	data = [int(line.removesuffix("\n")) for line in file]

for a in data:
	for b in data:
		if a + b == 2020:
			print(a * b)

[print(a * b * c) for a in data for b in data for c in data if a + b + c == 2020]
