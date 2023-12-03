import math
import re

input = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def get_no_border_coordinates(y: int, x: int, max_y: int, max_x: int):
    return [
        (y_, x_)
        for y_, x_ in [
            (y - 1, x),  # top
            (y - 1, x + 1),  # top right
            (y, x + 1),  # right
            (y + 1, x + 1),  # bottom right
            (y + 1, x),  # bottom
            (y + 1, x - 1),  # bottom left
            (y, x - 1),  # left
            (y - 1, x - 1),  # top left
        ]
        if 0 <= y_ <= max_y and 0 <= x_ <= max_x
    ]


def get_total_of_coherent_digits(input: str):
    total = 0
    input_array = input.strip().splitlines()
    max_y = len(input_array) - 1
    for y, line in enumerate(input_array):
        max_x = len(line) - 1
        coherent_digits = [(m.group(), m.span()) for m in re.finditer(r"\d+", line)]
        for digit, (start_x, end_x) in coherent_digits:
            symbol_adjacents: list[str] = []
            for x in range(start_x, end_x):
                for y_, x_ in get_no_border_coordinates(y, x, max_y, max_x):
                    if (char := input_array[y_][x_]) != "." and not char.isdigit():
                        symbol_adjacents.append(char)
            total += int(digit) if len(symbol_adjacents) else 0
    return total


assert get_total_of_coherent_digits(input) == 4361

with open("2023/3/input.txt") as f:
    print(get_total_of_coherent_digits(f.read()))


def get_total_of_adjacent_gears(input: str):
    total = 0
    input_list = input.strip().splitlines()
    max_y = len(input_list) - 1
    for y, line in enumerate(input_list):
        max_x = len(line) - 1
        gears = [m.start() for m in re.finditer(r"\*", line)]
        for x in gears:
            unique_numbers: set[int] = set()
            for y_, x_ in get_no_border_coordinates(y, x, max_y, max_x):
                if (char := input_list[y_][x_]).isdigit():
                    full_number = get_full_number(input_list, char, y_, x_)
                    unique_numbers.add(int(full_number))
            total += math.prod(unique_numbers) if len(unique_numbers) == 2 else 0
    return total


def get_full_number(input_list: list[str], part_number: str, y: int, x: int):
    part_number = get_left(input_list, part_number, y, x)
    part_number = get_right(input_list, part_number, y, x)
    return part_number


def get_left(input_list: list[str], part_number: str, y: int, x: int):
    if x - 1 < 0 or not (left := input_list[y][x - 1]).isdigit():
        return part_number
    part_number = f"{left}{part_number}"
    return get_left(input_list, part_number, y, x - 1)


def get_right(input_list: list[str], part_number: str, y: int, x: int):
    if x + 1 > len(input_list[y]) - 1 or not (right := input_list[y][x + 1]).isdigit():
        return part_number
    part_number = f"{part_number}{right}"
    return get_right(input_list, part_number, y, x + 1)


assert get_total_of_adjacent_gears(input) == 467835

with open("2023/3/input.txt") as f:
    print(get_total_of_adjacent_gears(f.read()))
