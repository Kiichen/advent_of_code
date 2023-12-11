input = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""


def get_sum_of_shortest_ranges(input: str, expand: int):
    grid = input.strip().splitlines()

    empty_rows = [y for y, row in enumerate(grid) if all(c == "." for c in row)]
    empty_cols = [
        x for x in range(len(grid[0])) if all(c == "." for row in grid for c in row[x])
    ]

    galaxies = [
        (y, x) for y, row in enumerate(grid) for x, col in enumerate(row) if col == "#"
    ]

    total = 0

    for i, galaxy in enumerate(galaxies):
        for other_galaxy in galaxies[:i]:
            y_1, x_1 = galaxy
            y_2, x_2 = other_galaxy

            if y_1 > y_2:
                y_1, y_2 = y_2, y_1
            if x_1 > x_2:
                x_1, x_2 = x_2, x_1

            for row in range(y_1, y_2):
                total += expand if row in empty_rows else 1
            for col in range(x_1, x_2):
                total += expand if col in empty_cols else 1

    return total


assert get_sum_of_shortest_ranges(input, 2) == 374

with open("2023/11/input.txt") as f:
    print(get_sum_of_shortest_ranges(f.read(), 2))

# assert get_sum_of_shortest_ranges(input, 1_000_000) == 8410

with open("2023/11/input.txt") as f:
    print(get_sum_of_shortest_ranges(f.read(), 1_000_000))
