input = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""


def get_hash_value(step: str):
    cur_val = 0
    for char in step:
        ascii_val = ord(char)
        cur_val += ascii_val
        cur_val *= 17
        cur_val = cur_val % 256
    return cur_val


def sum_of_hash(line: str):
    total = 0
    for step in line.split(","):
        total += get_hash_value(step)

    return total


assert sum_of_hash(input) == 1320

with open("2023/15/input.txt") as f:
    print(sum_of_hash(f.read()))


def get_boxes(line: str):
    boxes: dict[int, list[tuple[str, str]]] = {}
    for step in line.split(","):
        if "=" in step:
            label, value = step.split("=")
            box = get_hash_value(label)
            if box not in boxes:
                boxes[box] = [(label, value)]
            else:
                if any([l == label for l, _ in boxes[box]]):
                    boxes[box] = [
                        (l, value) if l == label else (l, v) for l, v in boxes[box]
                    ]
                else:
                    boxes[box].append((label, value))
        elif "-" in step:
            label, value = step.split("-")
            box = get_hash_value(label)
            if box in boxes:
                boxes[box] = [item for item in boxes[box] if item[0] != label]
    return boxes


def get_box_value(boxes: dict[int, list[tuple[str, str]]]):
    total = 0
    for box in boxes:
        for slot, (_, value) in enumerate(boxes[box]):
            val = (box + 1) * (slot + 1) * int(value)
            total += val
    return total


assert get_box_value(get_boxes(input)) == 145

with open("2023/15/input.txt") as f:
    print(get_box_value(get_boxes(f.read())))
