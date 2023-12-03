from template import get_fullstr_by_pointing_to_segment, line_to_list_of_ints
from template import get_neighbors, get_diagonals, rotate_grid
from template import create_3d_grid, get_3d_neighbors
def test_get_fullstr_by_pointing_to_segment():
    # line, index, chars, valid, expected
    tests = [
        ("abc123def456", 5, "1234567890", True, "123"),
        ("abc123def456", 2, "1234567890", False, "abc"),
        ("123abc", 0, "1234567890", True, "123"),
        ("abc123", 5, "1234567890", True, "123"),
        ("123abc", 0, "abc", False, "123"),
        ("abc123", 5, "abc", False, "123"),
        ("abc123", 1, "abc", False, ""),
        ("abc123", 0, "abc", False, ""),
        ("abc123", 0, "123", True, "")
    ]

    for i, test in enumerate(tests):
        line, index, chars, valid, expected = test
        result = get_fullstr_by_pointing_to_segment(line, index, chars, valid)
        status = "OK" if result == expected else "FAILED"
        print('[{}/{}] {} "{}" = "{}"'.format(i + 1, len(tests), status, result, expected))
        assert result == expected


def test_line_to_list_of_ints():
    # line, expected
    tests = [
        ("abc123def456", [123, 456]),
        ("123def456", [123, 456]),
        ("123abc", [123]),
        ("abc123", [123]),
        ("abc1.2.3", [1, 2, 3]),
        ("abc", [])
    ]

    for i, test in enumerate(tests):
        line, expected = test
        result = line_to_list_of_ints(line)
        status = "OK" if result == expected else "FAILED"
        print('[{}/{}] {} {} = {}'.format(i + 1, len(tests), status, result, expected))
        assert result == expected


def test_get_neighbors():
    data = [
        "123",
        "456",
        "789"
    ]
    grid: list[list] = [list(line) for line in data]
    tests = [
        (grid, 0, 0, ['4', '2']),
        (grid, 1, 1, ['2', '8', '4', '6']),
        (grid, 2, 0, ['4', '8']),
        (grid, 0, 2, ['6', '2']),
        (grid, 2, 2, ['6', '8']),
        (grid, 1, 2, ['3', '9', '5'])
    ]

    for i, test in enumerate(tests):
        grid, x, y, expected = test
        result = get_neighbors(grid, x, y)
        status = "OK" if result == expected else "FAILED"
        print('[{}/{}] {} {} = {}'.format(i + 1, len(tests), status, result, expected))
        assert result == expected

def test_get_diagonals():
    data = [
        "123",
        "456",
        "789"
    ]
    grid: list[list] = [list(line) for line in data]
    tests = [
        (grid, 0, 0, ['5']),
        (grid, 1, 1, ['1', '3', '7', '9']),
        (grid, 2, 0, ['5']),
        (grid, 0, 2, ['5']),
        (grid, 2, 2, ['5']),
        (grid, 1, 2, ['2', '8']),
        (grid, 1, 0, ['2', '8'])
    ]

    for i, test in enumerate(tests):
        grid, x, y, expected = test
        result = get_diagonals(grid, x, y)
        status = "OK" if result == expected else "FAILED"
        print('[{}/{}] {} {} = {}'.format(i + 1, len(tests), status, result, expected))
        assert result == expected


def test_rotate_grid():
    data_in = [
        "123",
        "456",
        "789"
    ]
    data_out = [
        "741",
        "852",
        "963"
    ]

    grid_in: list[list] = [list(line) for line in data_in]
    grid_out: list[list] = [list(line) for line in data_out]

    result = rotate_grid(grid_in)
    status = "OK" if result == grid_out else "FAILED"
    print('[1/1] {} {} = {}'.format(status, result, grid_out))
    assert result == grid_out

# Run the test function
test_get_fullstr_by_pointing_to_segment()
test_line_to_list_of_ints()
test_get_neighbors()
test_get_diagonals()
test_rotate_grid()

print(create_3d_grid(3, 2, 4, 0))
grid = [[
    [0, 1, 2, 3],
    [4, 5, 6, 7]
], [
    [8, 9, 10, 11],
    [12, 13, 14, 15]
], [
    [16, 17, 18, 19],
    [20, 21, 22, 23]
]]

grid = [
    [[0, 1, 2], [3, 4, 5], [6, 7, 8]],
    [[9, 10, 11], [12, 13, 14], [15, 16, 17]],
    [[18, 19, 20], [21, 22, 23], [24, 25, 26]]
]

print(grid[0][1][1])
print(sorted(get_3d_neighbors(grid, 0, 1, 1)))