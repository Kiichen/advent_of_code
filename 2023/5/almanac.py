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


def handle_group(lines: str, prev: list[int], start: str, end: str) -> list[int]:
    groups = get_groups(lines, start, end)
    ranges = convert_group_to_ranges(groups)
    return get_next_group(prev, ranges)


def get_lowest_location(input: str):
    lines = input.strip()

    seeds = get_groups(lines, "seeds:", "seed-to-soil map:")[0]
    seeds = list(map(int, seeds.split(" ")))

    soils = handle_group(lines, seeds, "seed-to-soil map:", "soil-to-fertilizer map:")
    fertilizers = handle_group(lines, soils, "soil-to-fertilizer map:", "fertilizer-to-water map:")
    waters = handle_group(lines, fertilizers, "fertilizer-to-water map:", "water-to-light map:")
    lights = handle_group(lines, waters, "water-to-light map:", "light-to-temperature map:")
    temperatures = handle_group(lines, lights, "light-to-temperature map:", "temperature-to-humidity map:")
    humidities = handle_group(lines, temperatures, "temperature-to-humidity map:", "humidity-to-location map:")
    locations = handle_group(lines, humidities, "humidity-to-location map:", "")

    return min(locations)


assert get_lowest_location(input) == 35

with open("2023/5/input.txt") as f:
    print(get_lowest_location(f.read()))
