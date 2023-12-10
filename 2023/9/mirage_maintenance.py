input = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def get_diffs(numbers: list[int]):
    diffs = []
    for i in range(0, len(numbers) - 1):
        diff = numbers[i + 1] - numbers[i]
        diffs.append(diff)
    return diffs


def get_sum_of_last(lines: str):
    total = 0
    for line in lines.strip().splitlines():
        numbers = [int(number) for number in line.split()]
        matrix = [numbers]
        while not all(diff == 0 for diff in numbers):
            numbers = get_diffs(numbers)
            matrix.append(numbers)

        matrix.reverse()
        for i, row in enumerate(matrix):
            prev = matrix[i - 1] if i != 0 else None
            matrix[i] = row + [row[-1] + prev[-1] if prev else 0]

        total += matrix[-1][-1]

    return total


assert get_sum_of_last(input) == 114

with open("2023/9/input.txt") as f:
    print(get_sum_of_last(f.read()))


def get_sum_of_first(lines: str):
    total = 0
    for line in lines.strip().splitlines():
        numbers = [int(number) for number in line.split()]
        matrix = [numbers]
        while not all(diff == 0 for diff in numbers):
            numbers = get_diffs(numbers)
            matrix.append(numbers)

        matrix.reverse()
        for i, row in enumerate(matrix):
            prev = matrix[i - 1] if i != 0 else None
            matrix[i] = [row[0] - prev[0] if prev else 0] + row

        total += matrix[-1][0]

    return total


assert get_sum_of_first(input) == 2

with open("2023/9/input.txt") as f:
    print(get_sum_of_first(f.read()))
