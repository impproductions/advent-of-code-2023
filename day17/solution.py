import math
from pathlib import Path
from pprint import pprint
import heapq

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines = input_file.read_text().splitlines()
map_ = {(x, y): int(v) for y, l in enumerate(lines) for x, v in enumerate(l)}
dirs = [(0, 1), (-1, 0), (0, -1), (1, 0)]


def travel(start, end, map_, min_dist, max_dist):
    queued = [(0, start, -1)]
    visited = set()
    heat_losses = {}
    while queued:
        heat_loss, pos, forbidden_dir = heapq.heappop(queued)
        if pos == end:
            return heat_loss
        if (pos, forbidden_dir) in visited:
            continue
        visited.add((pos, forbidden_dir))
        x, y = pos
        for dir in range(len(dirs)):
            streak_value = 0
            if dir == forbidden_dir or (dir + 2) % len(dirs) == forbidden_dir:
                continue
            for distance in range(1, max_dist + 1):
                new_x = x + dirs[dir][0] * distance
                new_y = y + dirs[dir][1] * distance
                new_pos = (new_x, new_y)
                if not new_pos in map_:
                    continue
                streak_value += map_[new_pos]
                if distance < min_dist:
                    continue
                tot_value = heat_loss + streak_value
                if tot_value < heat_losses.get((new_pos, dir), math.inf):
                    heat_losses[(new_pos, dir)] = tot_value
                    heapq.heappush(queued, (tot_value, new_pos, dir))


def part1():
    return travel((0, 0), max(map_), map_, 1, 3)


def part2():
    return travel((0, 0), max(map_), map_, 4, 10)


print(part1())
print(part2())
