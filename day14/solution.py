from functools import cache
from pathlib import Path
from pprint import pprint
import time


current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines = input_file.read_text().splitlines()


def roll(line, at_start=True):
    return "#".join(
        "".join(sorted(section, reverse=at_start)) for section in line.split("#")
    )


def flip(map_):
    return ["".join([row[c] for row in map_]) for c in range(len(map_[0]))]


def tilt(map_, dir):
    if dir in {"u", "d"}:
        return flip([roll(r, dir in {"u", "l"}) for r in flip(map_)])
    return [roll(r, dir in {"u", "l"}) for r in map_]


def cycle(map_):
    for i in range(4):
        map_ = tilt(tuple(map_), ["u", "l", "d", "r"][i % 4])
    return map_


def get_weights(map_):
    return sum([len(map_) - y for y, line in enumerate(map_) for c in line if c == "O"])


def part1():
    return get_weights(tilt(lines[:], "u"))


def part2():
    map_ = lines[:]
    maps, visited = {}, {}
    max = 1_000_000_000

    for i in range(max):
        map_ = tuple(cycle(map_))
        maps[i] = map_

        if map_ in visited:
            map_ = maps[visited[map_] - 1 + (max - visited[map_]) % (i - visited[map_])]
            return get_weights(map_)

        visited[map_] = i


print(part1())
print(part2())
