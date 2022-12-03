with open("input") as file:
	data = [line.removesuffix("\n") for line in file]

input_str = data

# Opponent: A for Rock, B for Paper, and C for Scissors
# Me:       X for Rock, Y for Paper, and Z for Scissors
# Score:    0 if you lost, 3 if the round was a draw, and 6 if you won
def score_match(a, b):
    if a == "A":
        match b:
            case "X":
                return 3
            case "Y":
                return 6
            case "Z":
                return 0
    if a == "B":
        match b:
            case "X":
                return 0
            case "Y":
                return 3
            case "Z":
                return 6
    if a == "C":
        match b:
            case "X":
                return 6
            case "Y":
                return 0
            case "Z":
                return 3


# Opponent: A for Rock, B for Paper, and C for Scissors
# Strategy: X: lose, Y: draw, Z: win
def get_response(a, b):
    if a == "A":
        if b == "X":
            return "Z"
        if b == "Y":
            return "X"
        if b == "Z":
            return "Y"

    if a == "B":
        if b == "X":
            return "X"
        if b == "Y":
            return "Y"
        if b == "Z":
            return "Z"

    if a == "C":
        if b == "X":
            return "Y"
        if b == "Y":
            return "Z"
        if b == "Z":
            return "X"


# 1 for Rock, 2 for Paper, and 3 for Scissors
def score_shape(a):
    if a == "X":
        return 1
    if a == "Y":
        return 2
    if a == "Z":
        return 3


total_score = 0
for game in input_str:
    opponent = game.split()[0]
    response = game.split()[1]
    total_score += (score_shape(response) + score_match(opponent, response))

print("Total score with interpretation  I of the secret strategy guide: " + str(total_score))

total_score = 0
for game in input_str:
    opponent = game.split()[0]
    order = game.split()[1]
    response = get_response(opponent, order)
    total_score += (score_shape(response) + score_match(opponent, response))

print("Total score with interpretation II of the secret strategy guide: " + str(total_score))
