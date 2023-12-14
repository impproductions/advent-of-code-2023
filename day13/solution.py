from gettext import find
from itertools import combinations
import math
from operator import is_
from pathlib import Path
from pprint import pprint
import re

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
maps = input_file.read_text().split("\n\n")


def find_centers(rows):
    candidates = [ri for ri in range(len(rows) - 1) if rows[ri] == rows[ri + 1]]
    centers = []

    # print("find centers for", rows)

    for candidate in candidates:
        i = 0
        is_valid = True
        while True:
            if candidate - i < 0 or candidate + i + 1 >= len(rows):
                break
            # print("comparing for candidate", candidate)
            # print(rows[candidate - i])
            # print(rows[candidate + i + 1])
            if rows[candidate - i] != rows[candidate + i + 1]:
                is_valid = False
                break
            i += 1
        if is_valid:
            centers.append(candidate)

    return centers


def part1():
    rows = []
    cols = []
    for i, m in enumerate(maps):
        map_rows = m.split("\n")
        map_cols = [
            "".join([row[c] for row in map_rows]) for c in range(len(map_rows[0]))
        ]

        rows.append(map_rows)
        cols.append(map_cols)

    row_centers = [find_centers(m) for m in rows]
    col_centers = [find_centers(m) for m in cols]
    print(row_centers)
    print(col_centers)
    # pprint(([c for c in row_centers if c], [c for c in col_centers if c]))

    totals = sum([sum([c + 1 for c in centers]) for centers in col_centers])
    totals += sum([sum([c + 1 for c in centers]) for centers in row_centers]) * 100

    return totals


def compare_rows(row1, row2):
    diffs = 0
    index = None
    for i in range(len(row1)):
        if row1[i] != row2[i]:
            if diffs > 0:
                return None
            index = i
            diffs += 1

    return (True, index)


def find_centers2(rows):
    candidates = [
        ri for ri in range(len(rows) - 1) if compare_rows(rows[ri], rows[ri + 1])
    ]
    centers = []

    print("find centers for")
    pprint(rows)
    
    print("candidates:")
    pprint(candidates)


    for candidate in candidates:
        i = 0
        is_valid = True
        has_cleaned = False
        while True:
            if candidate - i < 0 or candidate + i + 1 >= len(rows):
                break
            print("comparing for candidate", candidate)
            print(candidate - i, rows[candidate - i])
            print(candidate + i + 1, rows[candidate + i + 1])
            print("result", compare_rows(rows[candidate - i], rows[candidate + i + 1]), "valid", is_valid, "cleaned", has_cleaned)
            if not compare_rows(rows[candidate - i], rows[candidate + i + 1]):
                is_valid = False
                break
            elif compare_rows(rows[candidate - i], rows[candidate + i + 1])[0]:
                if rows[candidate - i] != rows[candidate + i + 1]:
                    if has_cleaned:
                        is_valid = False
                        break
                    else:
                        has_cleaned = True
            i += 1
        if is_valid:
            centers.append(candidate)

    return set(centers)


def part2():
    rows = []
    cols = []
    for i, m in enumerate(maps):
        map_rows = m.split("\n")
        map_cols = [
            "".join([row[c] for row in map_rows]) for c in range(len(map_rows[0]))
        ]

        rows.append(map_rows)
        cols.append(map_cols)

    og_row_centers = [set(find_centers(m)) for m in rows]
    og_col_centers = [set(find_centers(m)) for m in cols]

    # for mi, m in enumerate(rows):
    #     row_candidates = {
    #         (i, j): (r1, r2)
    #         for i, r1 in enumerate(m)
    #         for j, r2 in enumerate(m)
    #         if i != j and compare_rows(r1, r2)
    #     }
    #     row_candidates = {
    #         tuple(sorted((i, j)))
    #         for i, r1 in enumerate(m)
    #         for j, r2 in enumerate(m)
    #         if i != j and abs((i - j) % 2 != 0) and compare_rows(r1, r2)
    #     }
    #     # row_candidates = {math.floor((b - a) / 2) for a, b in row_candidates}

    #     print(mi, row_candidates)
    row_centers = [find_centers2(m) - og_row_centers[i] for i, m in enumerate(rows)]
    col_centers = [find_centers2(m) - og_col_centers[i] for i, m in enumerate(cols)]

    for i, cs in enumerate(col_centers):
        # if len(cs) > 1:
        #     for c in cs:
        #         pprint(cols[i])
        print("cols", i, cs, "og", og_col_centers[i])
    for i, cs in enumerate(row_centers):
        # if len(cs) > 1:
        #     for c in cs:
        #         pprint(rows[i])
        print("rows", i, cs, "og", og_row_centers[i])
    print(row_centers)
    print(col_centers)

    totals = sum(
        [sum([c + 1 for c in centers]) for i, centers in enumerate(col_centers)]
    )
    totals += (
        sum([sum([c + 1 for c in centers]) for i, centers in enumerate(row_centers)])
        * 100
    )

    return totals


print(part1())
print(part2())
