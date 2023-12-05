
def slice_seeds(seeds: set[tuple[int, int]], maps: set[tuple[int, int]]) -> set[tuple[int, int]]:
    split_seeds: list[tuple[int, int]] = list(seeds)
    for seed in split_seeds:
        a, b = seed
        for m in maps:
            s_1, s_2 = m
            if b <= s_1 or a >= s_2:
                continue
            else:
                split_seeds.remove((a, b))
                # map range (s_1, s_2) inside seed range (a, b)
                if a <= s_1 <= s_2 <= b:
                    split_seeds.append((a, s_1))
                    split_seeds.append((s_2, b))
                # left of seed range inside map range
                elif s_1 <= a < s_2:
                    split_seeds.append((a, s_2))
                    split_seeds.append((s_2, b))
                # right of seed range inside map range
                elif s_2 >= b > s_1:
                    split_seeds.append((a, s_1))
                    split_seeds.append((s_1, b))
                else:
                    print('slice {} {}, seed {},{}'.format(s_1, s_2, a, b))
                    raise Exception("This should not happen!")

seeds = {(1, 3), (6, 10)}
maps = {(3, 7)}
print(slice_seeds(seeds, maps))
