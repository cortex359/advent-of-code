with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

signal = data[0]
signal = "nppdvjthqldpwncqszvftbrmjlhg"

for v in range(len(signal)):
	package = signal[v:v+4]
	package_set = set(package)
	if len(package_set) == len(package):
		print(v+4)
		break

for v in range(len(signal)):
	package = signal[v:v+14]
	package_set = set(package)
	if len(package_set) == len(package):
		print(v+14)
		break