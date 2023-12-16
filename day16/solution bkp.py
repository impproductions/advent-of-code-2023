from functools import cache
from pathlib import Path
from pprint import pprint


def print_map(m, *highlight_conditions):
    xsize = max(x for x, _ in m) + 1
    ysize = max(y for _, y in m) + 1
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


current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines = input_file.read_text().splitlines()

map_ = {(x, y): value for y, line in enumerate(lines) for x, value in enumerate(line)}

elements = {
    (x, y): value
    for y, line in enumerate(lines)
    for x, value in enumerate(line)
    if value in {"/", "\\", "-", "|"}
}
row_blocking_elements = {
    y: [x for x, v in enumerate(l) if v in {"|", "\\", "/"}]
    for y, l in enumerate(lines)
}
col_blocking_elements = {
    x: [y for y, line in enumerate(lines) if line[x] in {"-", "\\", "/"}]
    for x in range(len(lines[0]))
}

blocking_map = {
    "col": col_blocking_elements,
    "row": row_blocking_elements,
}

map_size = (len(lines[0]), len(lines))

directions = {
    ("-", "u"): (
        "l",
        "r",
    ),
    ("-", "d"): (
        "l",
        "r",
    ),
    ("-", "l"): tuple(),
    ("-", "r"): tuple(),
    ("|", "l"): (
        "u",
        "d",
    ),
    ("|", "r"): (
        "u",
        "d",
    ),
    ("|", "u"): tuple(),
    ("|", "d"): tuple(),
    ("\\", "u"): ("r",),
    ("\\", "d"): ("l",),
    ("\\", "l"): ("d",),
    ("\\", "r"): ("u",),
    ("/", "u"): ("l",),
    ("/", "d"): ("r",),
    ("/", "l"): ("u",),
    ("/", "r"): ("d",),
}

dirs = {
    "r": (1, 0),
    "d": (0, 1),
    "l": (-1, 0),
    "u": (0, -1),
}


@cache
def beam(head):
    (x, y), dir = head
    dest = None
    energized = {(x, y)}

    if dir == "u":
        hits = [(x, by) for by in blocking_map["col"][x] if by < y]
        if hits:
            dest = max(hits)
        else:
            dest = (x, 0)
    elif dir == "d":
        hits = [(x, by) for by in blocking_map["col"][x] if by > y]
        if hits:
            dest = min(hits)
        else:
            dest = (x, map_size[1])
    elif dir == "l":
        hits = [(bx, y) for bx in blocking_map["row"][y] if bx < x]
        if hits:
            dest = max(hits)
        else:
            dest = (0, y)
    elif dir == "r":
        hits = [(bx, y) for bx in blocking_map["row"][y] if bx > x]
        if hits:
            dest = min(hits)
        else:
            dest = (map_size[0], y)

    dx, dy = dest
    xrange = range(*sorted((x, dx)))
    yrange = range(*sorted((y, dy)))
    energized = {(rx, y) for rx in xrange}
    energized = {(x, ry) for ry in yrange} | energized

    return dest, energized


opposite = {
    "u": "d",
    "l": "r",
    "r": "l",
    "d": "u",
}


def part1():
    energized = set()
    heads = {((-1, 0), "r")}

    visited_states = set()

    while len(heads) > 0:
        cycle_heads = set()
        cycle_energized = set()

        last_energized = energized.copy()
        for head in heads:
            coords, dir = head
            dest, new_energized = beam(head)
            # print("moved from", head, "to", dest)
            cycle_energized = cycle_energized | new_energized
            if dest in elements and dest != coords:
                elem = elements[dest]
                split_dirs = directions[(elem, opposite[dir])]
                cycle_heads = cycle_heads | {
                    (dest, split_dir) for split_dir in split_dirs
                }
                cycle_energized.add(dest)
        visited_states.add(tuple(heads))
        heads = cycle_heads
        energized = energized | cycle_energized

        if tuple(cycle_heads) in visited_states:
            break

    energized = energized - {(-1, 0)}

    return len(energized)


def part2():
    edges = {}
    edges["d"] = [(x, -1) for x in range(len(lines[0]))]
    edges["u"] = {(x, len(lines)) for x in range(len(lines[0]))}
    edges["r"] = {(-1, y) for y in range(len(lines))}
    edges["l"] = {(len(lines[0]), y) for y in range(len(lines))}

    totals = 0

    for startdir, edge in edges.items():
        # print("trying", startdir, edge)
        for point in edge:
            # print("trying", point, startdir)
            energized = set()
            start = point
            heads = {(start, startdir)}

            visited_states = set()

            while len(heads) > 0:
                cycle_heads = set()
                cycle_energized = set()

                last_energized = energized.copy()
                for head in heads:
                    coords, dir = head
                    dest, new_energized = beam(head)

                    cycle_energized = cycle_energized | new_energized
                    if dest in elements and dest != coords:
                        elem = elements[dest]
                        split_dirs = directions[(elem, opposite[dir])]
                        cycle_heads = cycle_heads | {
                            (dest, split_dir) for split_dir in split_dirs
                        }
                        cycle_energized.add(dest)
                visited_states.add(tuple(heads))
                heads = cycle_heads
                energized = energized | cycle_energized
                if tuple(cycle_heads) in visited_states:
                    break

            energized = energized - {start}

            # print("result", point, startdir, len(energized))
            totals = max(totals, len(energized))

    return totals


print(part1())
print(part2())
