with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

count = 0
for line in data:
	line = line.split(" ")
	a, b = line[0].split("-")
	letter = line[1].removesuffix(":")
	password = line[2]
	if int(a) <= password.count(letter) <= int(b):
		count += 1

# Part I
#print(count)

count2 = 0
for line in data:
	line = line.split(" ")
	a, b = line[0].split("-")
	letter = line[1].removesuffix(":")
	password = line[2]
	if (password[int(a) - 1] == letter and password[int(b) - 1] != letter) or (password[int(a) - 1] != letter and password[int(b) - 1] == letter):
		count2 += 1

print(count2)