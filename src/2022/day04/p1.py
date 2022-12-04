with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

contain_counter = 0
overlap_counter = 0
for line in data:
	a, b = [int(x) for x in line.split(",")[0].split("-")]
	c, d = [int(x) for x in line.split(",")[1].split("-")]

	# cd containing ab?
	if b-a < d-c:
		if a >= c and b <= d:
			contain_counter += 1
	# ab containing cd?
	if d-c <= b-a:
		if c >= a and d <= b:
			contain_counter += 1
	# overlaps?
	if (c <= a <= d) or (c <= b <= d) or (a <= c <= b) or (a <= d <= b):
		overlap_counter += 1

print("Assignment pairs fully containing the other: ", contain_counter)
print("Assignment pairs that overlap: ", overlap_counter)