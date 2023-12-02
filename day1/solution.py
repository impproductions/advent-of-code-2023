from pathlib import Path

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")

lines = input_file.read_text().splitlines()

ns = {str(d): d for d in range(10)}


def get_digit(line, index, rev):
    for n, nd in ns.items():
        to_check = (
            line[index : index + len(n)]
            if not rev
            else line[index - len(n) + 1 : index + 1]
        )
        if to_check == n:
            return nd


def get_digits(line):
    numbers = []
    for i in range(len(line)):
        if d := get_digit(line, i, False):
            numbers.append(d)
            break
    for i in range(len(line) - 1, 0, -1):
        if d := get_digit(line, i, True):
            numbers.append(d)
            break

    return int(f"{numbers[0]}{numbers[-1]}")


def part1():
    line_digits = [get_digits(l) for l in lines]
    return sum(line_digits)


def part2():
    ns.update(
        {
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
        }
    )
    line_digits = [get_digits(l) for l in lines]
    return sum(line_digits)


print(part1())
print(part2())
