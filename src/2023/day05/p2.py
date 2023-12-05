import re
import numpy as np
from collections import deque
from collections import defaultdict
import itertools

# d = defaultdict(int)  # Default to int (0)

with open("example") as file:
    data: list = [line.removesuffix("\n") for line in file]

# Regex Stuff
# -----------
def line_to_list_of_ints(line):
    """Convert a line of numbers to a list of ints"""
    return list(map(int, re.findall(r'\d+', line)))

#######################################################################

seed_range_list: list[tuple[int, int]] = []

if data[0].startswith("seeds: "):
    seed_list: list[int] = line_to_list_of_ints(data[0])
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


# for mappings
# seed_ranges -> slice -> convert -> repeat
# seed_ranges: list of (start, ende)

def slice_ranges(list_of_ranges: set, slice_start: int, slice_end: int) -> set:
    print('Running slice_ranges with list_of_ranges = {}'.format(list_of_ranges))
    list_of_ranges_to_iterate: list = list(list_of_ranges.copy())
    out_range_set: set = list_of_ranges.copy()
    # range list: (start, end)
    for index, range_start_end in enumerate(list_of_ranges_to_iterate):
        range_start, range_end = range_start_end
        # range is completely outside of slice
        if range_end <= slice_start or range_start >= slice_end:
            continue
        # range is completely inside of slice
        out_range_set.discard(range_start_end)
        if slice_start >= range_start and slice_end <= range_end:
            out_range_set.add((slice_start, slice_end))
            out_range_set.add((range_start, slice_start - 1))
            out_range_set.add((slice_end + 1, range_end))
        # range is partially inside of slice right side
        elif range_start < slice_start < range_end:
            out_range_set.add((range_start, slice_start))
            out_range_set.add((slice_start + 1, range_end))
        # range is partially inside of slice left side
        elif range_start < slice_end < range_end:
            out_range_set.add((range_start, slice_end))
            out_range_set.add((slice_end + 1, range_end))
    return out_range_set

def convert_range(erange, destination_start):
    return

# for all mappings
for key, mappings in maps.items():
    print(key, mappings)

    # slice accordingly
    print("Slicing…")
    original_seed_range_list = seed_range_list.copy()
    seed_range_set: set = set(seed_range_list)
    for i, src_range in enumerate(original_seed_range_list):
        print("list_of_source_ranges", src_range)
        for destination_start, source_start, range_length in mappings:
            seed_range_set = slice_ranges(seed_range_set, source_start, source_start + range_length)
    print("New seed range set: {}".format(sorted(seed_range_set)))

    # convert
    # destination range start, the source range start, and the range length
    print("Converting…")
    converted_ranges: set = set()
    for i, srcr in enumerate(seed_range_set):
        for destination_start, source_start, range_length in mappings:
            converted_ranges.add((
                srcr[0] + destination_start - source_start,
                srcr[1] + destination_start - source_start,
                range_length
            ))

    seed_range_list = converted_ranges

print(seed_range_list)
