from colorama import Fore
from colorama import Style

with open("input") as file:
    data = [line.removesuffix("\n") for line in file]


def compare_pkgs(left, right):
    if type(left) == int and type(right) == int:
        if left < right:
            # print("Right order")
            return 1
        elif left > right:
            # print("Wrong order")
            return -1
        else:
            # print("continue")
            return 0
    elif type(left) == list and type(right) == list:
        for l, r in zip(left, right):
            o = compare_pkgs(l, r)
            if o == 0:
                continue
            else:
                return o
        if len(left) < len(right):
            # print("Right order")
            return 1
        elif len(left) > len(right):
            # print("Wrong order")
            return -1
        else:
            return 0
    # print("continue")
    elif type(left) == int and type(right) == list:
        return compare_pkgs([left], right)
    elif type(left) == list and type(right) == int:
        return compare_pkgs(left, [right])


def bubble_sort(array):
    n = len(array)
    for i in range(n):
        already_sorted = True
        for j in range(n - i - 1):
            if compare_pkgs(array[j], array[j + 1]) == -1:
                array[j], array[j + 1] = array[j + 1], array[j]
                already_sorted = False
        if already_sorted:
            break
    return array


indices = []
packages = [[[2]], [[6]]]

for n, line in enumerate(data):
    if n % 3 == 0:
        left = eval(line)
        right = eval(data[n + 1])

        packages.append(left)
        packages.append(right)

        result = compare_pkgs(left, right)
        index = (n // 3) + 1
        if result == 1:
            # print(f"Pair {index:3d}: Right order")
            indices.append(index)
        elif result == -1:
            # print(f"Pair {index:3d}: Wrong order")
            pass
        else:
            print(f"Pair {index:3d}: No result {result}")

#       PART  I
# >>>>>>-------<<<<<<

# 5593 not right, 5503 right
print(f"There are {len(indices)} out of {(n // 3 + 1)} pair of packets already in the right order.\n"
      f"The sum of their indices is {Fore.YELLOW}{Style.BRIGHT}{sum(indices)}{Style.RESET_ALL}.")

#       PART II
# >>>>>>-------<<<<<<
packages = bubble_sort(packages)

divider_indices = [
    packages.index([[2]]) + 1,
    packages.index([[6]]) + 1
]
decoder_key = divider_indices[0] * divider_indices[1]

print(f"The divider packets are at {divider_indices[0]}th and {divider_indices[1]}th place.\nThe decoder key",
      f"for the distress signal is {Fore.GREEN}{Style.BRIGHT}{decoder_key}{Style.RESET_ALL}.")
