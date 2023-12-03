with open("input") as file:
    data = [line.removesuffix("\n") for line in file]

# Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green

id_sums = 0
mult_sums = 0

for line in data:
    game_id = line.split(": ")[0].split("Game ")[1]
    cubes = line.split(": ")[1].split("; ")
    # print(game_id, cubes)

    possible = True
    red_max, green_max, blue_max = 0, 0, 0
    for c in cubes:
        red, green, blue = 0, 0, 0
        for g in c.split(", "):
            # print("g:", g)
            num = g.split(" ")[0]
            if g.endswith("red"):
                red += int(num)
            elif g.endswith("green"):
                green += int(num)
            elif g.endswith("blue"):
                blue += int(num)
        # print(red, green, blue)

        red_max = max(red, red_max)
        green_max = max(green, green_max)
        blue_max = max(blue, blue_max)

    mult_sums += blue_max * red_max * green_max

    # Part 1:
    # 12 red cubes, 13 green cubes, and 14 blue
    if red_max <= 12 and green_max <= 13 and blue_max <= 14:
        # print(game_id, cubes)
        id_sums += int(game_id)

print(id_sums)
print(mult_sums)
