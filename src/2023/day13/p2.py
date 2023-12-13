import numpy as np

with open("input") as file:
    data: list = [line.strip() for line in file]


def display_pattern(grid) -> None:
    """Display a 2D Grid"""
    print("\nPattern:")
    for line in grid:
        print("".join(line))


def get_vertical_reflection_line(grid: np.ndarray) -> int:
    cols = grid.shape[1]
    for i in range(0, cols - 1):
        size = min(cols - i - 1, i + 1)
        left_section = grid[:, i - size + 1:i + 1]
        right_section = grid[:, i + 1:size + i + 1]
        # print(f"[{i}] {size} {left_section} {right_section}")
        # print(right_section, grid[:, cols:i])
        if np.sum(left_section != np.fliplr(right_section)) == 1:
            return i + 1
    return None


def get_horizontal_reflection_line(grid: np.ndarray) -> int:
    return get_vertical_reflection_line(np.rot90(grid))


summation = 0
pattern: list = []
for i, l in enumerate(data):
    if l == '' or i == len(data) - 1:
        grid: list[list] = [list(line) for line in pattern]

        vr = get_vertical_reflection_line(np.array(grid))
        hr = get_horizontal_reflection_line(np.array(grid))

        if vr:
            print(f"Vertical Reflection Line: {vr}")
            summation += vr
        if hr:
            print(f"Horizontal Reflection Line: {hr}")
            summation += hr * 100

        pattern = []
    else:
        pattern.append(list(l))

print(f"Summation: {summation}")
