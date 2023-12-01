import re


def get_first_and_last_digit(input: str):
    digits = [char for char in input if char.isdigit()]
    return int(f"{digits[0]}{digits[-1]}") if len(digits) else 0


def sum_lines(lines: str, func: callable):
    return sum([func(line) for line in lines.strip().splitlines()])


input = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

assert sum_lines(input, get_first_and_last_digit) == 142

with open("2023/1/input.txt") as f:
    print(sum_lines(f.read(), get_first_and_last_digit))

MAPPING = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def get_first_and_last_digit_with_words(input: str):
    regex = "|".join([*list(MAPPING.keys()), *list(MAPPING.values())])
    all_matches: list[str] = re.findall(f"(?=({regex}))", input)
    digits = [match if match.isdigit() else MAPPING[match] for match in all_matches]
    return int(f"{digits[0]}{digits[-1]}") if len(digits) else 0


input = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

assert sum_lines(input, get_first_and_last_digit_with_words) == 281

with open("2023/1/input.txt") as f:
    print(sum_lines(f.read(), get_first_and_last_digit_with_words))
