import re

with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

current_path: str = ""
dirs_found: set = set()
files_found: dict = {}
file_sizes: dict = {}
dir_sizes: dict = {}
list_mode: bool = False

for line in data:
	if line[0] == "$":
		list_mode = False
		if line[2:4] == "cd":
			if line[5:7] == "..":
				current_path = "/".join(current_path.split("/")[:-2])
			elif line[5:] == "/":
				current_path = "/"
			else:
				current_path += "/" + line[5:]
			current_path = re.sub("/{2,}", "/", current_path + "/")
			dirs_found.add(current_path)
		elif line[2:4] == "ls":
			list_mode = True
			continue
	elif list_mode:
		if line[0:4] == "dir":
			dirs_found.add(current_path + line[4:])
		elif re.search(r"^[0-9]+\s.*$", line):
			file_sizes[current_path + line.split()[1]] = line.split()[0]

total_size_sum = 0
dirs_counted = 0

used_space = 46876531
disk_space = 70000000
unused_space = disk_space - used_space
unused_space_needed = 30000000
space_to_free_up = unused_space_needed - unused_space

deletion_candidates: dict = {}

for d in list(dirs_found):
	dir_size = 0
	for f in [fm for fm in list(file_sizes.keys()) if fm.startswith(d)]:
		dir_size += int(file_sizes[f])
	dir_sizes[d] = dir_size
	if dir_size <= 100_000:
		total_size_sum += dir_size
		dirs_counted += 1
	if dir_size >= space_to_free_up:
		deletion_candidates[d] = dir_size

relevant_size_for_summation_marked: bool = False
relevant_size_for_deletion_marked: bool = False
for d, s in sorted(dir_sizes.items(), key=lambda item: item[1]):
	if not relevant_size_for_summation_marked:
		if int(s) >= 100_000:
			print(f"{'#'*65} {'Directories with size exceeding 100.000':>44} : {'#'*15}")
			relevant_size_for_summation_marked = True
	if not relevant_size_for_deletion_marked:
		if int(s) >= space_to_free_up:
			print(f"{'#'*65} {'Candidates for Deletion':>44} : {'#'*15}")
			relevant_size_for_deletion_marked = True
	print(f"{d:111s}: {s:15,d}")


print("\n--- Results ---")
print("Total size of all dirs with size less than 100,000:")
print(f"\tsize = {total_size_sum:,}\n\tdirs counted = {dirs_counted:,}\n\tof total dirs found = {len(dirs_found):,}")

d, s = sorted(deletion_candidates.items(), key=lambda item: item[1])[0]

print(f"Smallest directory that is at least {space_to_free_up:,} in size:\n\t{d}\n\tsize = {s:,}")
