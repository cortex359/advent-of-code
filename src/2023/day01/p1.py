import re

with open("input") as file:
    data = [line.removesuffix("\n") for line in file]

sum_cvs = 0

for line in data:
    cleand_line: str = re.sub(r'\D', '', line)
    calibration_value: int = int(cleand_line[0] + cleand_line[-1])
    print('{} → {} : {}'.format(line, cleand_line, calibration_value))
    sum_cvs += calibration_value

# → 54331
print(sum_cvs)
