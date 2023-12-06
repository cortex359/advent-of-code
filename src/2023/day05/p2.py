import re

with open("input") as file:
    data: list = [line.removesuffix("\n") for line in file]

seed_range_list: list[tuple[int, int]] = []

if data[0].startswith("seeds: "):
    seed_list: list[int] = list(map(int, re.findall(r'\d+', data[0])))
print(seed_list)

summing = 0
for i, s in enumerate(seed_list):
    if i % 2 == 0 and i < len(seed_list) - 1:
        # (start, end)
        seed_range_list.append((seed_list[i], seed_list[i] + seed_list[i+1]))
        summing += seed_list[i+1]
print(summing)
## Total seed numbers: 2631174522

maps: dict = {
    "seed-soil":[],
    "soil-fertilizer":[],
    "fertilizer-water":[],
    "water-light":[],
    "light-temperature":[],
    "temperature-humidity":[],
    "humidity-location":[]
}

for line in data[2:]:
    if line.endswith("map:"):
        destination, source = line.replace(" map:", "").split("-to-")
        print(destination, source)
    elif line != "":
        destination_start, source_start, range_length = line.split(" ")
        maps[f"{destination}-{source}"].append((int(destination_start), int(source_start), int(range_length)))

print("#############")

# for mappings
# seed_ranges -> slice -> convert -> repeat
# seed_ranges: list of (start, ende)

def slice_ranges(a: set[tuple[int, int]], b: set[tuple[int, int]]) -> set[tuple[int, int]]:
    boundaries: set[int] = set()
    for i in a.union(b):
        boundaries.add(i[0])
        boundaries.add(i[1])

    sliced_boundaries: set[tuple[int, int]] = set()
    boundary_list = sorted(list(boundaries))
    for i in range(len(boundary_list) - 1):
        for s in a:
            if s[0] <= boundary_list[i] < boundary_list[i + 1] <= s[1]:
                # we have a boundary inside a
                sliced_boundaries.add((boundary_list[i], boundary_list[i + 1]))

    return sliced_boundaries

def convert_range(erange, delta):
    return (erange[0] + delta, erange[1] + delta)

# for all mappings
for key, mappings in maps.items():
    print("key={}, mappings={}".format(key, mappings))

    # slice accordingly
    print("Slicing…")
    original_seed_range_list = seed_range_list.copy()
    seed_range_set: set = set(seed_range_list)
    # destination range start, the source range start, and the range length

    map_intervalls = [(source_start, source_start + range_length) for _, source_start, range_length in mappings]
    seed_range_set = slice_ranges(seed_range_set, map_intervalls)
    print("New seed range set: {}".format(sorted(seed_range_set)))

    # convert
    # destination range start, the source range start, and the range length
    print("Converting…")
    converted_ranges: set = set()
    for seed_range in seed_range_set:
        converted = False
        for destination_start, source_start, range_length in mappings:
            if seed_range[0] >= source_start and seed_range[1] <= source_start + range_length:
                converted_ranges.add(convert_range(seed_range, destination_start - source_start))
                converted = True
                break

        if not converted:
            converted_ranges.add(seed_range)

    print("converted_ranges:", converted_ranges)
    seed_range_list = converted_ranges

print("converted seed_range_list: {}".format(sorted(seed_range_list)))
print("min: {}".format(min(seed_range_list)[0]))
