with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

freq = [0,0,0,0,0,0,0,0,0,0,0]

# Example
#data = ["00100", "11110", "10110", "10111", "10101", "01111", "00111", "11100", "10000", "11001", "00010", "01010"]
#freq = [0,0,0,0,0]

for l in data:
	for i in range(len(l)-1):
		if int(l[i]) == 1:
			freq[i] += 1

print(len(data))
isize = len(data)
print(freq)

gamma_rate = ""
epsilon_rate = ""
for f in freq:
	if f > (isize/2):
		gamma_rate += "1"
		epsilon_rate += "0"
	else:
		gamma_rate += "0"
		epsilon_rate += "1"

print("Gamma: " + str(int(gamma_rate, 2)))
print("Epsilon: " + str(int(epsilon_rate, 2)))
print("Mult.: " + str(int(gamma_rate, 2) * int(epsilon_rate, 2)))


# oxygen generator rating
ogr = data

pos = 0
while len(ogr) > 1 and pos < len(ogr[0]):
	freq = len([i for i in ogr if i[pos] == "1"])
	if freq >= (len(ogr)/2):
		ogr = [x for x in ogr if x[pos] == "1"]
	else:
		ogr = [x for x in ogr if x[pos] == "0"]
	pos += 1

print(pos)
print("OGR: ", ogr, "\n in dec: ", int(ogr[0], 2))

# CO2 scrubber rating
cosr = [s.strip() for s in data]

pos = 0
while len(cosr) > 1 and pos < len(cosr[0]):
	freq = len([i for i in cosr if i[pos] == "0"])
	if freq <= (len(cosr)/2):
		cosr = [x for x in cosr if x[pos] == "0"]
	else:
		cosr = [x for x in cosr if x[pos] == "1"]
	pos += 1

print(pos)
print("CO2 SR: ", cosr, "\n in dec: ", int(cosr[0], 2))

print("Life support rating: ", (int(ogr[0], 2) * int(cosr[0], 2)))