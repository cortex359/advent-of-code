def slice_ranges(a: set[tuple[int, int]], b: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """slices a set of intervals into subintervals, such that all subintervals are either inside or outside every
    interval in set b"""
    tupels: tuple[int] = tuple()
    for i in a.union(b):
        tupels += i

    sliced_boundaries: set[tuple[int, int]] = set()
    boundary_list: list[int] = sorted(list(set(tupels)))

    for i in range(len(boundary_list) - 1):
        for s in a:
            if s[0] <= boundary_list[i] < boundary_list[i + 1] <= s[1]:
                sliced_boundaries.add((boundary_list[i], boundary_list[i + 1]))

    return sliced_boundaries


seeds = {(1, 5), (6, 10), (12, 15)}
maps = {(3, 7), (12, 13)}
# [(1, 3), (3, 5), (6, 7), (7, 10), (12, 13), (13, 15)]
print(sorted(slice_ranges(seeds, maps)))

