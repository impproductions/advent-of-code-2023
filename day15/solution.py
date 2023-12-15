from functools import cache, reduce
from pathlib import Path
from pprint import pprint


current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines = input_file.read_text()

steps = lines.split(",")


def hash(string):
    return reduce(lambda p, c: ((p + ord(c)) * 17) % 256, [0, *string])


def find_index(label, box):
    for i, content in enumerate(box):
        if content[0] == label:
            return i


def part1():
    return sum([hash(step) for step in steps])


def part2():
    boxes = {}
    for step in steps:
        if step[-1] != "-":
            label, focus = step.split("=")
            focus, box = int(focus), hash(label)
            boxes[box] = boxes.get(box, [])
            if (lens_index := find_index(label, boxes[box])) is not None:
                boxes[box][lens_index] = (label, focus)
            else:
                boxes[box].append((label, focus))
        else:
            label = step[:-1]
            box = hash(label)
            if box in boxes:
                if (index := find_index(label, boxes[box])) is not None:
                    del boxes[box][index]
    totals = [
        (i + 1) * sum([(j + 1) * c[1] for j, c in enumerate(b)])
        for i, b in boxes.items()
    ]
    return sum(totals)


print(part1())
print(part2())
