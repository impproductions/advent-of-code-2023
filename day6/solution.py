from math import sqrt, prod, ceil
from pathlib import Path
from pprint import pprint
import re

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines = input_file.read_text().splitlines()

times = list(map(int, re.findall(r"\d+", lines[0])))
distances = list(map(int, re.findall(r"\d+", lines[1])))
races = [(times[i], distances[i]) for i in range(len(times))]


def bounds_size(t, d):
    lower = ceil((-t + sqrt(t**2 - (4 * d))) / -2)
    upper = ceil((-t - sqrt(t**2 - (4 * d))) / -2)

    return len(range(lower, upper))


def part1():
    ways_to_win = [bounds_size(t, d) for t, d in races]

    return prod(ways_to_win)


def part2():
    t = int("".join([str(t) for t in times]))
    d = int("".join([str(d) for d in distances]))

    return bounds_size(t, d)


print(part1())
print(part2())
