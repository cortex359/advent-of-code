with open("input") as file:
    data: list = [line.removesuffix("\n") for line in file]

########################################################################################################################

# A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2
strength_rev = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
strength = list(reversed(strength_rev))

def evaluate_hand(line, delta):
    hand = line.split(" ")[0]

    print(delta)
    # Five of a kind
    if hand[0] == hand[1] == hand[2] == hand[3] == hand[4]:
        return 100 + delta
    sorted_hand = sorted(hand)
    # Four of a kind
    if sorted_hand[0] == sorted_hand[1] == sorted_hand[2] == sorted_hand[3]:
        return 85 + delta
    elif sorted_hand[1] == sorted_hand[2] == sorted_hand[3] == sorted_hand[4]:
        return 85 + delta
    # Full house
    if sorted_hand[0] == sorted_hand[1] == sorted_hand[2] and sorted_hand[3] == sorted_hand[4]:
        return 70 + delta
    if sorted_hand[0] == sorted_hand[1] and sorted_hand[2] == sorted_hand[3] == sorted_hand[4]:
        return 70 + delta
    # Three of a kind
    if sorted_hand[0] == sorted_hand[1] == sorted_hand[2]:
        return 55 + delta
    elif sorted_hand[1] == sorted_hand[2] == sorted_hand[3]:
        return 55 + delta
    elif sorted_hand[2] == sorted_hand[3] == sorted_hand[4]:
        return 55 + delta
    # Two pair
    if sorted_hand[0] == sorted_hand[1] and sorted_hand[2] == sorted_hand[3]:
        return 40 + delta
    elif sorted_hand[0] == sorted_hand[1] and sorted_hand[3] == sorted_hand[4]:
        return 40 + delta
    elif sorted_hand[1] == sorted_hand[2] and sorted_hand[3] == sorted_hand[4]:
        return 40 + delta
    # One pair
    if sorted_hand[0] == sorted_hand[1]:
        return 25 + delta
    elif sorted_hand[1] == sorted_hand[2]:
        return 25 + delta
    elif sorted_hand[2] == sorted_hand[3]:
        return 25 + delta
    elif sorted_hand[3] == sorted_hand[4]:
        return 25 + delta
    # High card
    return delta


def evaluate_hand_with_J(line):
    hand = line.split(" ")[0]
    delta = (strength.index(hand[0]) + strength.index(hand[1])/15 + strength.index(hand[2])/225
             + strength.index(hand[3])/3375 + strength.index(hand[4])/50625)

    max_eva = 0
    for card in strength_rev:
        max_eva = max(max_eva, evaluate_hand(line.replace("J", card), delta))
    return max_eva
def sort_poker_hands(hands):
    return sorted(hands, key=evaluate_hand_with_J, reverse=False)

ranked_poker_hands = sort_poker_hands(data)

summation = 0
for i, hand in enumerate(ranked_poker_hands):
    print('[{}] {}'.format(i+1, hand))
    summation += (i+1) * int(hand.split(" ")[1])

print(summation)

