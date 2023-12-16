from pathlib import Path
from pprint import pprint

L, U, R, D = 0, 1, 2, 3

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines = input_file.read_text().splitlines()
map_size = (len(lines[0]), len(lines))

elements = {
    (x, y): value
    for y, line in enumerate(lines)
    for x, value in enumerate(line)
    if value in {"/", "\\", "-", "|"}
}

directions = {
    ("-", U): (L, R),
    ("-", D): (L, R),
    ("-", L): (),
    ("-", R): (),
    ("|", L): (U, D),
    ("|", R): (U, D),
    ("|", U): (),
    ("|", D): (),
    ("\\", U): (R,),
    ("\\", D): (L,),
    ("\\", L): (D,),
    ("\\", R): (U,),
    ("/", U): (L,),
    ("/", D): (R,),
    ("/", L): (U,),
    ("/", R): (D,),
}


def connect(head):
    (x, y), dir = head
    dest = None
    energized = {(x, y)}

    if dir == U:
        dest = (x, 0)
        for by in range(y - 1, 0, -1):
            if elements.get((x, by), None) in {"\\", "/", "-"}:
                dest = (x, by)
                break
    elif dir == D:
        dest = (x, map_size[1])
        for by in range(y + 1, map_size[1]):
            if elements.get((x, by), None) in {"\\", "/", "-"}:
                dest = (x, by)
                break
    elif dir == L:
        dest = (0, y)
        for bx in range(x - 1, 0, -1):
            if elements.get((bx, y), None) in {"\\", "/", "|"}:
                dest = (bx, y)
                break
    elif dir == R:
        dest = (map_size[0], y)
        for bx in range(x + 1, map_size[0]):
            if elements.get((bx, y), None) in {"\\", "/", "|"}:
                dest = (bx, y)
                break

    dx, dy = dest
    xrange, yrange = range(*sorted((x, dx))), range(*sorted((y, dy)))
    energized = {(rx, y) for rx in xrange} | {(x, ry) for ry in yrange}
    if dx < map_size[0] and dy < map_size[1]:
        energized.add(dest)

    return dest, energized


edges = {}
edges[D] = [(x, -1) for x in range(len(lines[0]))]
edges[U] = [(x, len(lines)) for x in range(len(lines[0]))]
edges[R] = [(-1, y) for y in range(len(lines))]
edges[L] = [(len(lines[0]), y) for y in range(len(lines))]

connections = {(el, dir): connect((el, dir)) for el in elements for dir in {L, U, R, D}}
connections.update({(p, dir): connect((p, dir)) for dir, e in edges.items() for p in e})


def opposite(dir):
    return (dir + 2) % 4


def travel(head):
    heads = {head}
    energized, visited_states, contributors = set(), set(), set()

    while len(heads) > 0:
        cycle_heads = set()

        for head in heads:
            coords, dir = head
            dest, _ = connections[head]
            contributors.add(head)
            if dest in elements and dest != coords:
                elem = elements[dest]
                split_dirs = directions[(elem, opposite(dir))]
                for h in {(dest, split_dir) for split_dir in split_dirs}:
                    cycle_heads.add(h)
        visited_states.add(tuple(heads))
        heads = cycle_heads
        if tuple(cycle_heads) in visited_states:
            break

    energized = set()
    for c in contributors:
        for p in connections[c][1]:
            energized.add(p)

    return len(energized) - 1


def part1():
    return travel(((-1, 0), R))


def part2():
    totals = 0

    for startdir, edge in edges.items():
        for point in edge:
            energized = travel((point, startdir))
            totals = max(totals, energized)

    return totals


print(part1())
print(part2())
