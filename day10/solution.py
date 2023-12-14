import re
from pathlib import Path
from pprint import pprint

current_dir = Path(__file__).parent
input_file = Path(current_dir, "example2.txt")
lines = input_file.read_text().splitlines()
mapped = {(x, y): value for y, line in enumerate(lines) for x, value in enumerate(line)}
dirs = {
    "r": (1, 0),
    "d": (0, 1),
    "l": (-1, 0),
    "u": (0, -1),
}
pipes = {
    "|": {dirs["u"], dirs["d"]},
    "-": {dirs["l"], dirs["r"]},
    "F": {dirs["d"], dirs["r"]},
    "7": {dirs["d"], dirs["l"]},
    "J": {dirs["l"], dirs["u"]},
    "L": {dirs["r"], dirs["u"]},
    ".": [],
}


def add(p1, p2):
    return (
        p1[0] + p2[0],
        p1[1] + p2[1],
    )


def subtract(p1, p2):
    return (
        p1[0] - p2[0],
        p1[1] - p2[1],
    )


def get_neighbors(points: list[tuple[int]]) -> set[tuple[int]]:
    return {
        new_point
        for p in points
        for d in dirs.values()
        if (new_point := add(p, d)) in mapped
    }


def get_connected(point):
    return {add(point, conn) for conn in pipes[mapped[point]]}


def get_connections(point) -> list[tuple[int]]:
    neighbors = get_neighbors([point])
    neighbor_connections = {n: get_connected(n) for n in neighbors}
    connected = {k for k, v in neighbor_connections.items() if point in v}
    return {subtract(conn, point) for conn in connected}


start = [k for k, v in mapped.items() if v == "S"][0]
mapped[start] = [k for k, v in pipes.items() if v == set(get_connections(start))][0]


def travel(start):
    prev, current = start, get_connected(start).pop()
    loop = {start}
    while current != start:
        loop.add(current)
        connected = get_connected(current) - {prev}
        prev, current = current, connected.pop()
    return loop


def get_hits(point, dir, loop):
    curr, next = point, add(point, dir)
    hits = ""
    while next in mapped:
        if next in loop:
            hits += mapped[next]
        curr = next
        next = add(curr, dir)
    return hits


def print_map(m, *highlight_conditions):
    xsize, ysize = max(m)
    chart = ""
    for y in range(ysize):
        for x in range(xsize):
            c = m[(x, y)]
            for condition, replace in highlight_conditions:
                if condition((x, y)):
                    c = replace(m[(x, y)]) if callable(replace) else replace
            chart += c
        chart += "\n"
    print(chart)


def prettify(c):
    char = {
        "7": "┐",
        "L": "└",
        "J": "┘",
        "F": "┌",
        "|": "│",
        "-": "─",
        ".": " ",
    }
    return char[c]


def part1():
    loop = travel(start)
    print_map(
        mapped,
        (lambda x: not (x in loop), " "),
        (lambda x: x in loop, prettify),
    )
    return len(loop) // 2


def part2():
    loop = travel(start)
    inside = set()
    for point in mapped:
        if point in loop:
            continue
        hits = get_hits(point, dirs["r"], loop).replace("-", "")
        sides = hits.count("|")
        angles = len(re.findall(r"(L7|FJ)", hits))
        if (angles + sides) > 0 and (angles + sides) % 2 == 1:
            inside.add(point)
    print_map(
        mapped,
        (lambda x: x in inside, "I"),
        (lambda x: not x in inside, "O"),
        (lambda x: x in loop, prettify),
    )
    return len(inside)


print(part1())
print(part2())
