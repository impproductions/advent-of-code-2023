from pathlib import Path

current_dir = Path(__file__).parent
input_file = Path(current_dir, 'example1.txt')

lines = input_file.read_text().splitlines()

def part1():
    pass

def part2():
    pass

print(part1())
print(part2())