input = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

card_hands = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]


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


def get_score(input: str):
    lines = input.strip().splitlines()
    hands: list[Hand] = []
    for line in lines:
        hand, bid = line.split()
        bid = int(bid)

        hand_amounts = {}
        for card in hand:
            if card in hand_amounts:
                hand_amounts[card] += 1
            else:
                hand_amounts[card] = 1

        fives = [amount == 5 for amount in hand_amounts.values()]
        quads = [amount == 4 for amount in hand_amounts.values()]
        triples = [amount == 3 for amount in hand_amounts.values()]
        pairs = [amount == 2 for amount in hand_amounts.values()]

        highest_match = [
            any(fives),
            any(quads),
            any_fullhouse := any(triples) and any(pairs),
            any(triples) and not any_fullhouse,
            sum(pairs) == 2,
            sum(pairs) == 1,
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
