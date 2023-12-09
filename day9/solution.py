from functools import reduce
from pathlib import Path
from pprint import pprint

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines = input_file.read_text().splitlines()

seqs = [[*map(int, l.split(" "))] for l in lines]


def get_col_from_triangle(seq, col_index):
    col = [seq[col_index]]
    while any(seq):
        new_seq = [seq[i] - seq[i - 1] for i in range(1, len(seq))]
        col.append(new_seq[col_index])
        seq = new_seq
    return col


def part1():
    return sum([sum(get_col_from_triangle(s, -1)) for s in seqs])


def part2():
    return sum(
        reduce(lambda a, b: b - a, col[::-1])
        for col in [get_col_from_triangle(s, 0) for s in seqs]
    )


print(part1())
print(part2())
