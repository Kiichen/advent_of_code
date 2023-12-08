from math import lcm

input = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""


class Path:
    def __init__(self, key: str, left: str, right: str):
        self.key = key
        self.L = left
        self.R = right


class HauntedWasteland:
    def __init__(self, input: str) -> None:
        self.instructions, lines = input.strip().split("\n\n")
        self.paths = self.get_paths(lines)

    def handle_1(self):
        self.end_con = lambda path_key: path_key == "ZZZ"
        cur_path = [path for path in self.paths if path.key == "AAA"][0]
        return self.get_ways_count(cur_path)

    def handle_2(self):
        self.end_con = lambda path_key: path_key[-1] == "Z"
        cur_paths = [path for path in self.paths if path.key[-1] == "A"]
        ways = [self.get_ways_count(cur_path) for cur_path in cur_paths]
        return lcm(*ways)

    def get_paths(self, lines: str):
        paths: list[Path] = []
        for line in lines.splitlines():
            key, directions = line.split(" = ")
            left, right = directions[1:-1].split(", ")
            paths.append(Path(key, left, right))
        return paths

    def get_ways_count(self, cur_path: Path):
        end = False
        count = 0
        while not end:
            for instruction in self.instructions:
                count += 1

                next_path_key = getattr(cur_path, instruction)
                if self.end_con(next_path_key):
                    end = True
                    break

                for path in self.paths:
                    if path.key == next_path_key:
                        cur_path = path
                        break
        return count


assert HauntedWasteland(input).handle_1() == 6

with open("2023/8/input.txt") as f:
    print(HauntedWasteland(f.read()).handle_1())

input_2 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""


assert HauntedWasteland(input_2).handle_2() == 6

with open("2023/8/input.txt") as f:
    print(HauntedWasteland(f.read()).handle_2())
