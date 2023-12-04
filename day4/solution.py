from pathlib import Path
from pprint import pprint

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines: list[str] = input_file.read_text().splitlines()

cards = [
    (
        {int(n) for n in winning.split(": ")[1].split(" ") if n != ""},
        {int(n) for n in has.split(" ") if n != ""},
    )
    for winning, has in [line.split(" | ") for line in lines]
]


def part1():
    points = [2 ** (amt - 1) for w, h in cards if (amt := len(w & h)) > 0]
    return sum(points)


def part2():
    winners = [len(w & h) for w, h in cards]
    totals = {}
    for i, amt in enumerate(winners):
        limit = min(amt, len(cards) - i) + 1
        instances = [i + j for j in range(1, limit)]
        own_amt = totals.get(i, 0) + 1
        for has in instances:
            totals[has] = totals.get(has, 0) + own_amt
        totals[i] = own_amt
    return sum(totals.values())


print(part1())
print(part2())
