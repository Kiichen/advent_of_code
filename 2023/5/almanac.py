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


def get_groups(lines: str, start: str, end: str) -> list[str]:
    return lines[lines.find(start) + len(start) : lines.rfind(end)].strip().splitlines()


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


def handle_group(lines: str, prev: list[int], start: str, end: str) -> list[int]:
    groups = get_groups(lines, start, end)
    ranges = convert_group_to_ranges(groups)
    return get_next_group(prev, ranges)


def handle_group_ranges(lines: str, prev: list[tuple[int, int]], start: str, end: str) -> list[tuple[int, int]]:
    groups = get_groups(lines, start, end)
    ranges = convert_group_to_ranges(groups)
    return get_next_range_group(prev, ranges)


def get_lowest_location(input: str, get_seeds: callable, handle: callable):
    lines = input.strip()

    seeds = get_seeds(lines)

    soils = handle(lines, seeds, "seed-to-soil map:", "soil-to-fertilizer map:")
    fertilizers = handle(lines, soils, "soil-to-fertilizer map:", "fertilizer-to-water map:")
    waters = handle(lines, fertilizers, "fertilizer-to-water map:", "water-to-light map:")
    lights = handle(lines, waters, "water-to-light map:", "light-to-temperature map:")
    temperatures = handle(lines, lights, "light-to-temperature map:", "temperature-to-humidity map:")
    humidities = handle(lines, temperatures, "temperature-to-humidity map:", "humidity-to-location map:")
    locations = handle(lines, humidities, "humidity-to-location map:", "")
    return min(locations)


def get_seeds_as_lines(lines: str) -> list[int]:
    seeds = get_groups(lines, "seeds:", "seed-to-soil map:")[0]
    return list(map(int, seeds.split(" ")))


def get_seeds_as_pairs(lines: str) -> list[tuple[int, int]]:
    seeds = get_groups(lines, "seeds:", "seed-to-soil map:")[0]
    seeds = seeds.split(" ")
    actual = []
    for index, seed in enumerate(seeds):
        odd = (index % 2) == 0
        if not odd:
            prev = int(seeds[index - 1])
            actual.append((prev, prev + int(seed) - 1))

    return actual


assert get_lowest_location(input, get_seeds_as_lines, handle_group) == 35

with open("2023/5/input.txt") as f:
    print(get_lowest_location(f.read(), get_seeds_as_lines, handle_group))

assert get_lowest_location(input, get_seeds_as_pairs, handle_group_ranges)[0] == 46

with open("2023/5/input.txt") as f:
    print(get_lowest_location(f.read(), get_seeds_as_pairs, handle_group_ranges)[0])
