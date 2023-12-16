from pathlib import Path
from pprint import pprint
import re

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines = input_file.read_text().splitlines()

data = [(l.split(" ")[0], [*map(int, l.split(" ")[1].split(","))]) for l in lines]

# pprint(data)


from typing import List


def insert_zeros(array: List[int], num_zeros: int) -> List[List[int]]:
    def backtrack(index: int, path: List[int], zeros_remaining: int):
        if index == len(array):
            results.append(path + [0] * zeros_remaining)
            return

        min_zeros = 1 if index > 0 else 0
        for zeros_to_insert in range(min_zeros, zeros_remaining - (len(array) - index - 1) + 1):
            new_path = path + [0] * zeros_to_insert + [array[index]]
            backtrack(index + 1, new_path, zeros_remaining - zeros_to_insert)

    results = []
    backtrack(0, [], num_zeros)
    return results


def part1():
    arrs = []
    for records, lengths in data:
        zeroes = len(records) - sum(lengths)
        possible_arrangements = insert_zeros(lengths, zeroes)
        as_arrangements = ["".join([n * "#" if n > 0 else "." for n in arr]) for arr in possible_arrangements]
        regex = re.compile(records.replace(".", "\\.").replace("?", "."))
        keep = [arr for arr in as_arrangements if re.match(regex, arr)]
        arrs.append(len(keep))
        print("record", records, zeroes)
        print("arrs", len(keep))


    return sum(arrs)

data = [("?".join([l.split(" ")[0]] * 5), [*map(int, ",".join([l.split(" ")[1]] * 5).split(","))]) for l in lines]

def part2():
    arrs = []
    for records, lengths in data:
        print(len([r for r in records if r == "?"]))
        # zeroes = len(records) - sum(lengths)
        # possible_arrangements = insert_zeros(lengths, zeroes)
        # as_arrangements = ["".join([n * "#" if n > 0 else "." for n in arr]) for arr in possible_arrangements]
        # regex = re.compile(records.replace(".", "\\.").replace("?", "."))
        # # print(regex, records)
        # keep = [arr for arr in as_arrangements if re.match(regex, arr)]
        # arrs.append(len(keep))
        # print("record", records, zeroes)
        # print("arrs", len(keep))
        
        # pprint(possible_arrangements)

    return sum(arrs)

# print(part1())
print(part2())
