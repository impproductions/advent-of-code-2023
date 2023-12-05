import enum
from pathlib import Path
from pprint import pprint

from numpy import sort

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
text = input_file.read_text()
maps = [m.splitlines() for m in text.split("\n\n")[1:]]
maps = [sorted([[*map(int, r.split(" "))] for r in m[1:]]) for m in maps]
seeds = [*map(int, text.splitlines()[0].split(" ")[1:])]


def get_destination(seed, map):
    for dest, source, rng in map:
        if source <= seed < (source + rng):
            return dest + (seed - source)
    return seed


def part1():
    locations = []
    for seed in seeds:
        loc = seed
        for map in maps:
            loc = get_destination(loc, map)
        locations.append(loc)
    return min(locations)


def get_destinations(minseed, maxseed, map):
    return (get_destination(minseed, map), get_destination(maxseed, map))


def to_range(s, l):
    return (s, s + l)


def split(rng, parts):
    start, end = rng
    points = [start] + [part for part in parts if start < part < end]
    if end > points[-1]:
        points += [end]

    return [(points[i], points[i + 1]) for i in range(len(points) - 1)]


def split_ranges(ranges, breakpoints):
    return [part for rng in ranges for part in split(rng, sorted(breakpoints))]


def part2():
    ranges = [to_range(*seeds[i : i + 2]) for i in range(0, len(seeds), 2)]
    destinations = ranges
    for map in maps:
        breakpoints = (
            [  # use ranges instead of breakpoints to support non-continuous ranges
                src if (i < len(map) - 1) else (src + rng)
                for i, (_, src, rng) in enumerate(map)
            ]
        )
        ranges = split_ranges(destinations, breakpoints)
        destinations = [*{get_destinations(*rng, map) for rng in ranges}]

    return min([d[0] for d in destinations if d[0]])


print(part1())
print(part2())