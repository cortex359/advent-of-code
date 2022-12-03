with open("input") as file:
	data = list(map(int, [line.removesuffix("\n") for line in file]))

prev = 99999999999
counter = 0

for line in data:
	if line > prev:
		counter += 1
	prev = line

print(counter)

prev = 99999999999
counter = 0

for i in range(1, len(data)):
	measurewindows = sum(data[(i-1):(i+2)])
	if measurewindows > prev:
		counter += 1
	prev = measurewindows

if measurewindows > prev:
	counter += 1

print(counter)
