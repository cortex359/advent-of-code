with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

cycle = 0
x = 1
signal_strengths = 0
display: list[str] = []
row: str = ""

for line in data:
	for c in range(1 if line.split()[0] == "noop" else 2):
		cycle += 1
		if (cycle - 20) % 40 == 0:
			print(f"{cycle:4n} : {cycle * x:4n}")
			signal_strengths += cycle * x

		if len(row) in range(x-1, x+2):
			row += "o"
		else:
			row += " "
		if len(row) == 40:
			display.append(row)
			row = ""

	if line.split()[0] == "addx":
		x += int(line.split()[1])

print(f"Sum of signal strengths: {signal_strengths}")
print("Display:")
print(*display, sep="\n")