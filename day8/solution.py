import math
from pathlib import Path
from pprint import pprint

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines = input_file.read_text().splitlines()

directions = [0 if c == "L" else 1 for c in lines[0]]
maps = {
    loc: (*sides[1:-1].split(", "),)
    for loc, sides in (l.split(" = ") for l in lines[2:])
}


def travel(starting_points):
    z_visits = set()

    for location in starting_points:
        i = 0
        while location[-1] != "Z":
            location = maps[location][directions[i % len(directions)]]
            i += 1
        else:
            z_visits.add(i)

    return math.lcm(*z_visits)


def part1():
    return travel(["AAA"])


def part2():
    return travel([l for l in maps.keys() if l[-1] == "A"])


print(part1())
print(part2())
