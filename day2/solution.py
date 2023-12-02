import math
from pathlib import Path
from pprint import pprint

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")


lines = input_file.read_text().splitlines()
constraint_line = "12 red, 13 green, 14 blue"


def parse_set(dice_set: str):
    return {
        color: int(amt) for amt, color in (s.split(" ") for s in dice_set.split(", "))
    }

games = {
    int(gid.split(" ")[1]): [parse_set(s) for s in game.split("; ")]
    for gid, game in (l.split(": ") for l in lines)
}

constraint = parse_set(constraint_line)


def part1():
    possible = [
        gid
        for gid, game in games.items()
        if not any(
            any(amt > constraint[dice] for dice, amt in dice_set.items())
            for dice_set in game
        )
    ]

    return sum(possible)


def min_dice_set(game):
    res = [
        max([s[color] for s in game if s.get(color)])
        for color in ["red", "blue", "green"]
    ]
    return res


def part2():
    min_games = [math.prod(min_dice_set(game)) for game in games.values()]
    return sum(min_games)


print(part1())
print(part2())
