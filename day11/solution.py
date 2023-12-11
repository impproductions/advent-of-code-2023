from itertools import combinations
from pathlib import Path
from pprint import pprint

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines = input_file.read_text().splitlines()

galaxies = {
    (x, y)
    for y, line in enumerate(lines)
    for x, point in enumerate(line)
    if point == "#"
}
pairs = set(combinations(galaxies, 2))
empty_rows = {y for y, line in enumerate(lines) if all(p == "." for p in line)}
empty_cols = {x for x in range(len(lines[0])) if all([l[x] == "." for l in lines])}


def get_distance(a, b, expansion):
    xa, xb = sorted((a[0], b[0]))
    ya, yb = sorted((a[1], b[1]))
    dx = abs(xb - xa) + len(empty_cols & set(range(xa, xb))) * expansion
    dy = abs(yb - ya) + len(empty_rows & set(range(ya, yb))) * expansion

    return dx + dy


def part1():
    distances = {p: get_distance(*p, 1) for p in pairs}
    return sum(distances.values())


def part2():
    distances = {p: get_distance(*p, 1000000 - 1) for p in pairs}
    return sum(distances.values())


print(part1())
print(part2())
