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


class Grid:
    max_y: int
    max_x: int

    def __init__(self, max_y: int, max_x: int) -> None:
        self.max_y = max_y
        self.max_x = max_x


class Coordinate:
    y: int
    x: int
    grid: Grid

    def __init__(self, y: int, x: int, grid) -> None:
        self.y = y
        self.x = x
        self.grid = grid

    def get_surroundings(self):
        return [
            (y_, x_)
            for y_, x_ in [
                (self.y - 1, self.x),  # top
                (self.y - 1, self.x + 1),  # top right
                (self.y, self.x + 1),  # right
                (self.y + 1, self.x + 1),  # bottom right
                (self.y + 1, self.x),  # bottom
                (self.y + 1, self.x - 1),  # bottom left
                (self.y, self.x - 1),  # left
                (self.y - 1, self.x - 1),  # top left
            ]
            if 0 <= y_ <= self.grid.max_y and 0 <= x_ <= self.grid.max_x
        ]


class Symbol:
    char: str
    coordinates: list[tuple[int, int]]

    def __init__(self, char: str, coordinates: tuple[int, int]) -> None:
        self.char = char
        self.coordinates = coordinates


class Number:
    digit: str
    coordinates: list[Coordinate]
    symbol_adjacents: list[Symbol]

    def __init__(self, digit: str) -> None:
        self.digit = digit
        self.coordinates = []
        self.symbol_adjacents = []

    def get_symbol_coordinates(self):
        return [symbol.coordinates for symbol in self.symbol_adjacents]


class GearRatios:
    input_list: list[str]
    numbers: list[Number]
    gears: list[Symbol]
    grid: Grid

    def __init__(self, input: str) -> None:
        self.input_list = input.strip().splitlines()
        self.grid = Grid(len(self.input_list) - 1, len(self.input_list[0]) - 1)
        self.numbers = []
        self.gears = []

    def get_total_of_coherent_digits(self):
        self.set_numbers()
        return self.process_numbers()

    def get_total_of_adjacent_gears(self):
        self.set_numbers()
        self.set_gears()
        return self.process_gears()

    def set_numbers(self):
        for y, line in enumerate(self.input_list):
            coherent_digits = [(m.group(), m.span()) for m in re.finditer(r"\d+", line)]
            for digit, (start_x, end_x) in coherent_digits:
                number = Number(digit)
                for x in range(start_x, end_x):
                    number.coordinates.append(coordinate := Coordinate(y, x, self.grid))
                    number.symbol_adjacents.extend(
                        Symbol(c, (y_, x_))
                        for y_, x_ in coordinate.get_surroundings()
                        if (c := self.input_list[y_][x_]) != "." and not c.isdigit()
                    )
                self.numbers.append(number)

    def process_numbers(self):
        return sum(
            [
                int(number.digit)
                for number in self.numbers
                if len(number.symbol_adjacents)
            ]
        )

    def set_gears(self):
        self.gears = [
            Symbol("*", (y, x))
            for y, line in enumerate(self.input_list)
            for x, char in enumerate(line)
            if char == "*"
        ]

    def process_gears(self):
        return sum(
            math.prod(numbers_that_have_gear_as_adjacent)
            if len(
                numbers_that_have_gear_as_adjacent := [
                    int(number.digit)
                    for number in self.numbers
                    if gear.coordinates in number.get_symbol_coordinates()
                ]
            )
            == 2
            else 0
            for gear in self.gears
        )


assert GearRatios(input).get_total_of_coherent_digits() == 4361

with open("2023/3/input.txt") as f:
    print(GearRatios(f.read()).get_total_of_coherent_digits())


assert GearRatios(input).get_total_of_adjacent_gears() == 467835

with open("2023/3/input.txt") as f:
    print(GearRatios(f.read()).get_total_of_adjacent_gears())
