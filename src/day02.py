from utils.api import get_input

input_str = get_input(2)

# A for Rock, B for Paper, and C for Scissors
# X for Rock, Y for Paper, and Z for Scissors

def outcome(a, b):
    if(a == "A" and b == "X"):
        return 3
    if(a == "A" and b == "Y"):
        return 6
    if(a == "A" and b == "Z"):
        return 0

    if(a == "B" and b == "X"):
        return 0
    if(a == "B" and b == "Y"):
        return 3
    if(a == "B" and b == "Z"):
        return 6

    if(a == "C" and b == "X"):
        return 6
    if(a == "C" and b == "Y"):
        return 0
    if(a == "C" and b == "Z"):
        return 3


# A for Rock, B for Paper, and C for Scissors
#  X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win.
def followrule(a, b):
    if(a == "A" and b == "X"):
        return "Z"
    if(a == "A" and b == "Y"):
        return "X"
    if(a == "A" and b == "Z"):
        return "Y"

    if(a == "B" and b == "X"):
        return "X"
    if(a == "B" and b == "Y"):
        return "Y"
    if(a == "B" and b == "Z"):
        return "Z"

    if(a == "C" and b == "X"):
        return "Y"
    if(a == "C" and b == "Y"):
        return "Z"
    if(a == "C" and b == "Z"):
        return "X"


def score_shape(a):
    if(a == "X"):
        return 1
    if(a == "Y"):
        return 2
    if(a == "Z"):
        return 3

total_score = 0

for l in input_str:
    opponent = l.split()[0]
    response = l.split()[1]
    total_score += (score_shape(response) + outcome(opponent, response))

print(total_score)
#  shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

total_score = 0

for l in input_str:
    opponent = l.split()[0]
    order = l.split()[1]
    response = followrule(opponent, order)
    total_score += (score_shape(response) + outcome(opponent, response))

print(total_score)
