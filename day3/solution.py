import math
from pathlib import Path
from pprint import pprint
from string import digits

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines: list[str] = input_file.read_text().splitlines()


dirs = [(x, y) for x in (0, -1, 1) for y in (0, -1, 1)][1:]


def is_digit(c):
    return c in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}


def add(p1, p2):
    return (
        p1[0] + p2[0],
        p1[1] + p2[1],
    )


mapped = {(x, y): value for y, line in enumerate(lines) for x, value in enumerate(line)}
operators = {
    p: value for p, value in mapped.items() if not is_digit(value) and value != "."
}


def get_neighbors(points: list[tuple[int]]) -> set[tuple[int]]:
    return {
        new_point for p in points for d in dirs if (new_point := add(p, d)) in mapped
    }


def get_whole_number(point: tuple[int]) -> (int, set(tuple[int])):
    if not is_digit(mapped[point]):
        return None

    num_digits = mapped[point]
    num_points = {point}
    i = 1
    while mapped.get(r := add(point, (i, 0))) and is_digit(mapped[r]):
        num_digits += str(mapped[r])
        num_points.add(r)
        i += 1

    i = 1
    while mapped.get(l := add(point, (-i, 0))) and is_digit(mapped[l]):
        num_digits = str(mapped[l]) + num_digits
        num_points.add(l)
        i += 1

    return int(num_digits), num_points


def get_operators(num_coords: set[tuple[int]]):
    return {
        mapped[n]
        for n in get_neighbors(num_coords)
        if (mapped[n] != "." and not is_digit(mapped[n]))
    }


def get_neighboring_numbers(point):
    return {
        tuple(coords): n
        for p in get_neighbors([point])
        if (whole := get_whole_number(p))
        for n, coords in [whole]
    }


def part1():
    operators_with_numbers = {p: get_neighboring_numbers(p) for p in operators}
    return sum([n for ns in operators_with_numbers.values() for n in ns.values()])


def part2():
    operators_with_numbers = {
        p: ns[0] * ns[1]
        for p, value in operators.items()
        if value == "*"
        and (ns := list(get_neighboring_numbers(p).values()))
        and len(ns) > 1
    }

    return sum(operators_with_numbers.values())


print(part1())
print(part2())
