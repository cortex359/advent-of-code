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

seeds = {(1, 3), (6, 10)}
maps = {(3, 7)}
print(sorted(slice_ranges(seeds, maps)))

