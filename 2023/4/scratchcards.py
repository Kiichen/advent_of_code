from collections import defaultdict

input = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


def get_matches_of_line(line: str):
    data = line.split(": ")[1].split(" | ")

    winning_numbers = [number for number in data[0].split(" ") if number]
    owning_numbers = [number for number in data[1].split(" ") if number]

    return set(owning_numbers).intersection(winning_numbers)


def get_winning_pow(input: str):
    cards = input.strip().splitlines()

    total = 0
    for line in cards:
        matches = get_matches_of_line(line)

        pow_points = 0
        for _ in range(0, len(matches)):
            pow_points = pow_points + 1 if pow_points == 0 else pow_points * 2
        total += pow_points
    return total


assert get_winning_pow(input) == 13

with open("2023/4/input.txt") as f:
    print(get_winning_pow(f.read()))


def get_copies(input: str):
    cards = input.strip().splitlines()
    cards_dict: defaultdict[int, int] = defaultdict()

    for index, line in enumerate(cards):
        matches = get_matches_of_line(line)
        copies = cards_dict.setdefault(index, 1)

        for i in range(0, len(matches)):
            next_game = index + i + 1
            count = cards_dict.get(next_game, 1)
            if count is None:
                continue
            cards_dict.update({next_game: count + 1 * copies})
    return sum(cards_dict.values())


assert get_copies(input) == 30

with open("2023/4/input.txt") as f:
    print(get_copies(f.read()))
