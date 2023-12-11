import re
from pathlib import Path
from pprint import pprint

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
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
    return {add(conn, [-c for c in point]) for conn in connected}


start = [k for k, v in mapped.items() if v == "S"][0]
mapped[start] = [k for k, v in pipes.items() if v == set(get_connections(start))][0]


def next_point(point, next):
    while point in mapped:
        yield add(point, next)


def travel(start):
    prev, current = start, get_connected(start).pop()
    loop = {start}
    while current != start:
        loop.add(current)
        prev, current = current, get_connected(current) - {prev}

    return loop


def get_hits(point, dir, loop):
    return "".join(mapped[n] for n in next_point(point, dir) if n in loop)


def part1():
    loop = travel(start)

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

    return len(inside)


print(part1())
print(part2())
