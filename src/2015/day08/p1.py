import re

with open("input") as file:
    data: list[str] = [line.removesuffix("\n") for line in file]

chars_of_string_code = 0
chars_in_memory = 0

for line in data:
    chars_in_memory += len(line)
    escaped_string = re.sub(r'(^"|"$)', '', line)
    escaped_string = re.sub(r'\\\\|\\"|\\x[0-9a-f]{2}', 'x', escaped_string)
    chars_of_string_code += len(escaped_string)

print(f"chars in memory: {chars_in_memory}")
print(f"chars of string code: {chars_of_string_code}")
print(f"difference: {chars_in_memory - chars_of_string_code}")

chars_escaped = 0
for line in data:
    escaped_string = re.sub(r'\\', r'\\\\', line)
    escaped_string = re.sub(r'"', '\\"', escaped_string)
    escaped_string = re.sub(r'^(.*)$', r'"\1"', escaped_string)
    print(escaped_string)
    chars_escaped += len(escaped_string)

print(f"encoded length: {chars_escaped}")
print(f"difference: {chars_escaped - chars_in_memory}")