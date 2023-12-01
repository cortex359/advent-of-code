with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

passport: dict[str, str] = {}
passports: list = [passport]

#print(data)

for line in data:
	if line == "":
		passports.append(passport.copy())
		passport.clear()
		continue
	for k, v in [tuple(p.split(':')) for p in line.split(' ')]:
		passport[k] = v

passports.append(passport.copy())

valid_passports = 0
needed_keys = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])

for p in passports:
	if len(needed_keys.difference(p.keys())) != 0:
		print(needed_keys.difference(p.keys()), str(p.keys()))
		valid_passports += 1

print('{} out of {} passports'.format(valid_passports, len(passports)))