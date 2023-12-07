from collections import Counter


input = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


class Hand:
    bid: int
    value: str
    highest_match: int
    rank: int

    def __init__(self, bid: int, value: str, highest_match: int):
        self.bid = bid
        self.value = value
        self.highest_match = highest_match
        self.rank = None


def get_score(input: str, joker=False):
    card_hands = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    if joker:
        card_hands.append(card_hands.pop(card_hands.index("J")))

    lines = input.strip().splitlines()
    hands: list[Hand] = []

    for line in lines:
        hand, bid = line.split()
        bid = int(bid)

        if joker:
            joker_count = hand.count("J")

        hand_amounts = Counter(hand.replace("J", "") if joker else hand)

        if joker:
            if not hand_amounts.values():
                hand_amounts["J"] = joker_count
            else:
                max_key = max(hand_amounts, key=hand_amounts.get)
                hand_amounts[max_key] += joker_count

        highest_match = [
            5 in hand_amounts.values(),
            4 in hand_amounts.values(),
            3 in hand_amounts.values() and 2 in hand_amounts.values(),
            3 in hand_amounts.values() and 2 not in hand_amounts.values(),
            2 in hand_amounts.values() and list(hand_amounts.values()).count(2) == 2,
            2 in hand_amounts.values() and list(hand_amounts.values()).count(2) == 1,
            True,
        ].index(True)
        hands.append(Hand(bid, hand, highest_match))

    hands.sort(
        key=lambda hand: (
            hand.highest_match,
            [card_hands.index(card) for card in hand.value],
        )
    )

    rank = len(hands)
    for sorted_hand in hands:
        sorted_hand.rank = rank
        rank -= 1

    return sum([hand.bid * hand.rank for hand in hands])


assert get_score(input) == 6440

with open("2023/7/input.txt") as f:
    print(get_score(f.read()))


assert get_score(input, True) == 5905

with open("2023/7/input.txt") as f:
    print(get_score(f.read(), True))
