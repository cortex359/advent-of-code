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


def slice_seeds(seeds: set[tuple[int, int]], maps: set[tuple[int, int]]) -> set[tuple[int, int]]:
    ergebnis: set[tuple[int, int]] = set()

    for interval1 in seeds:
        a, b = interval1
        teilintervalle: set[tuple[int, int]] = {interval1}

        for interval2 in maps:
            s_1, s_2 = interval2
            neue_teilintervalle: set[tuple[int, int]] = set()

            if b <= s_1 or a >= s_2:
                neue_teilintervalle.add((a, b))
                continue
            else:
                # map range (s_1, s_2) inside seed range (a, b)
                if a <= s_1 <= s_2 <= b:
                    neue_teilintervalle.add((a, s_1))
                    neue_teilintervalle.add((s_2, b))
                # left of seed range inside map range
                elif s_1 <= a < s_2:
                    neue_teilintervalle.add((a, s_2))
                    neue_teilintervalle.add((s_2, b))
                # right of seed range inside map range
                elif s_2 >= b > s_1:
                    neue_teilintervalle.add((a, s_1))
                    neue_teilintervalle.add((s_1, b))
                else:
                    print('slice {} {}, seed {},{}'.format(s_1, s_2, a, b))
                    raise Exception("This should not happen!")

            print(neue_teilintervalle)
            teilintervalle.union(neue_teilintervalle)

        print("Teilintervalle:" + str(teilintervalle))
        ergebnis.union(teilintervalle)

    return ergebnis


# Beispiel
seeds = {(1, 5), (6, 10)}
maps = {(3, 7)}
print(slice_seeds(seeds, maps))

print(slice_ranges(seeds, 3, 7))

# (1, 3)(4, 5), (6, 7), (8, 10)