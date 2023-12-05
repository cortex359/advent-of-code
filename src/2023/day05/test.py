def slice_ranges(list_of_ranges, slice_start, slice_end):
    list_of_ranges_to_iterate = list_of_ranges.copy()
    for index, range_start_end in enumerate(list_of_ranges_to_iterate):
        range_start, range_end = range_start_end
        # range is completely outside of slice
        if range_end <= slice_start or range_start >= slice_end:
            continue
        # range is completely inside of slice
        if slice_start >= range_start and slice_end <= range_end:
            list_of_ranges[index] = (slice_start, slice_end)
            list_of_ranges.insert(index - 1, (range_start, slice_start - 1))
            list_of_ranges.insert(index + 2, (slice_end + 1, range_end))
        # range is partially inside of slice right side
        elif slice_start < range_start < slice_end:
            list_of_ranges[index] = (slice_start, range_start)
            list_of_ranges.insert(index + 1, (range_start + 1, slice_end))
        # range is partially inside of slice left side
        elif slice_start < range_end < slice_end:
            list_of_ranges[index] = (range_end, slice_end)
            list_of_ranges.insert(index, (slice_start, range_end - 1))
    return list_of_ranges

lof = [(1, 10), (11, 20)]
print(slice_ranges(lof, 10, 12))
