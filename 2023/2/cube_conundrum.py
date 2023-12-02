input = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

DEFAULT_MAP = {"red": 0, "blue": 0, "green": 0}
BOUNDS = {"red": 12, "green": 13, "blue": 14}


def get_sum_of_ids(input: str):
    total = 0
    for line in input.strip().splitlines():
        _id = line.split("Game")[1].split(":")[0].strip()
        pass_game = True

        for subset in line.split(":")[1].strip().split("; "):
            CUBE_MAP = DEFAULT_MAP.copy()
            for item in subset.split(", "):
                amount, color = item.split(" ")
                CUBE_MAP[color] += int(amount)
            if any(CUBE_MAP.get(key) > BOUNDS.get(key) for key in CUBE_MAP.keys()):
                pass_game = False
        if pass_game:
            total += int(_id)
    return total


assert get_sum_of_ids(input) == 8

with open("2023/2/input.txt") as f:
    print(get_sum_of_ids(f.read()))


def get_least_power_of_cubes(input: str):
    total = 0
    for line in input.strip().splitlines():
        MAX_CUBE_MAP = DEFAULT_MAP.copy()

        for subset in line.split(":")[1].strip().split("; "):
            CUBE_MAP = DEFAULT_MAP.copy()
            for item in subset.split(", "):
                amount, color = item.split(" ")
                CUBE_MAP[color] += int(amount)
            for key in CUBE_MAP.keys():
                MAX_CUBE_MAP[key] = max(CUBE_MAP.get(key), MAX_CUBE_MAP.get(key))

        power = 1
        for key in MAX_CUBE_MAP.keys():
            power *= MAX_CUBE_MAP.get(key)
        total += power
    return total


assert get_least_power_of_cubes(input) == 2286

with open("2023/2/input.txt") as f:
    print(get_least_power_of_cubes(f.read()))
