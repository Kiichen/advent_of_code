input = """
Time:      7  15   30
Distance:  9  40  200
"""


def get_ways_of_record_beating(input: str, merge=False):
    lines = input.strip().splitlines()

    times = list(map(int, lines[0].split("Time:")[1].strip().split()))
    records = list(map(int, lines[1].split("Distance:")[1].strip().split()))

    if merge:
        times = [int("".join(map(str, times)))]
        records = [int("".join(map(str, records)))]

    total = 1

    for time, record in zip(times, records):
        possible_wins = 0
        for speed in range(1, time):
            rest_mm = time - speed
            distance = speed * rest_mm
            if distance > record:
                possible_wins += 1
        total *= possible_wins
    return total


assert get_ways_of_record_beating(input) == 288

with open("2023/6/input.txt") as f:
    print(get_ways_of_record_beating(f.read()))

assert get_ways_of_record_beating(input, True) == 71503

with open("2023/6/input.txt") as f:
    print(get_ways_of_record_beating(f.read(), True))
