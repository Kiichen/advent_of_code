input = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


def convert_group_to_ranges(groups: list[str]) -> list[tuple[int, int, int]]:
    ranges = []
    for group in groups:
        destination, source, length = map(int, group.split())
        ranges.append((destination, source, length))
    return ranges


def get_next_group(current: list[int], ranges: list[tuple[int, int, int]]) -> list[int]:
    next_group = []
    for item in current:
        for destination, source, length in ranges:
            if source <= item <= source + length - 1:
                offset = source - destination
                newval = item - offset
                break
            else:
                newval = item
        next_group.append(newval)
    return next_group


def get_next_range_group(current: list[tuple[int, int]], ranges: list[tuple[int, int, int]]) -> list[tuple[int, int]]:
    next_group = []
    for start, end in current:
        for destination, source, length in ranges:
            group_max = max(start, source)
            group_min = min(end, source + length)
            if group_min > group_max:
                offset = source - destination
                range_start = group_max - offset
                range_end = group_min - offset
                new_val = (range_start, range_end)
                if start < group_max:
                    current.append((start, group_max))
                if end > group_min:
                    current.append((group_min, end))
                break
            else:
                new_val = (start, end)
        next_group.append(new_val)
    return next_group


def get_lowest_location(input: str, get_seeds: callable, handle: callable):
    lines = input.strip()

    seeds, *groups = lines.split("\n\n")

    next_group = get_seeds(seeds)

    for group in groups:
        group = group.split("\n")[1:]
        ranges = convert_group_to_ranges(group)
        next_group = handle(next_group, ranges)

    return min(next_group)


def get_seeds_as_lines(seeds: str) -> list[int]:
    seeds = seeds.split(": ")[1]
    return list(map(int, seeds.split(" ")))


def get_seeds_as_pairs(seeds: str) -> list[tuple[int, int]]:
    seeds = seeds.split(": ")[1]
    seeds = seeds.split(" ")
    actual = []
    for index, seed in enumerate(seeds):
        odd = (index % 2) == 0
        if not odd:
            prev = int(seeds[index - 1])
            actual.append((prev, prev + int(seed) - 1))

    return actual


assert get_lowest_location(input, get_seeds_as_lines, get_next_group) == 35

with open("2023/5/input.txt") as f:
    print(get_lowest_location(f.read(), get_seeds_as_lines, get_next_group))

assert get_lowest_location(input, get_seeds_as_pairs, get_next_range_group)[0] == 46

with open("2023/5/input.txt") as f:
    print(get_lowest_location(f.read(), get_seeds_as_pairs, get_next_range_group)[0])
