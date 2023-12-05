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


# import enum
# from pathlib import Path
# from pprint import pprint

# current_dir = Path(__file__).parent
# input_file = Path(current_dir, "input.txt")
# text = input_file.read_text()
# maps: list[str] = text.split("\n\n")[1:]
# maps = [m.splitlines() for m in maps]
# maps = [sorted([list(map(int, r.split(" "))) for r in m[1:]]) for m in maps]
# # # print(maps)
# seeds = list(map(int, text.splitlines()[0].split(" ")[1:]))


# def get_destination(seed, map):
#     for dest, source, rng in map:
#         if seed >= source and seed < (source + rng):
#             # # print("seed:", seed, "map:", map, "dest:", dest + (seed - source))
#             return dest + (seed - source)
#     return seed


# def get_destinations(minseed, maxseed, map):
#     return (get_destination(minseed, map), get_destination(maxseed, map))


# def get_location(seed):
#     loc = seed
#     for map in maps:
#         loc = get_destination(loc, map)
#         # # print(loc)
#     return loc


# def part1():
#     return min([get_location(seed) for seed in seeds])


# def to_range(s, l):
#     return (s, s + l)


# def split_range(src_range, sorted_breaks: list[tuple[int]]):
#     points = [src_range[0]]
#     points = points + [
#         start
#         for bk in sorted_breaks
#         if (start := bk[0]) >= points[-1] and start < src_range[1]
#     ]
#     points = points + [end] if (end := sorted_breaks[-1][-1]) < src_range[1] and end > points[-1] else points
#     points = points + [last] if (last := src_range[1]) > points[-1] else points
#     # print("breakpoints", points)
#     return [
#         (point, points[i + 1]) for i, point in enumerate(points) if i < len(points) - 1
#     ]


# def split_ranges(src_ranges, over: list[tuple[int]]):
#     sorted_over = sorted(over)
#     return [rng for r in src_ranges for rng in split_range(r, sorted_over)]


# def part2():
#     ranges = [
#         to_range(seeds[i], seeds[i + 1]) for i, seed in enumerate(seeds) if i % 2 == 0
#     ]
#     destinations = ranges
#     for i, m in enumerate(maps):
#         for_split = [to_range(s, r) for d, s, r in m]
#         ranges = split_ranges(destinations, for_split)
#         destinations = tuple(set([get_destinations(d_r[0], d_r[1], m) for d_r in ranges]))

#     return min([d[0] for d in destinations if d[0] != 0])

# print(part1())
# print(part2())
