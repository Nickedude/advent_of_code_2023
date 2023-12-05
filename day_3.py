from dataclasses import dataclass
from typing import List, Tuple, Set


@dataclass
class Part:
    number: int
    row: int
    col: int

    def __hash__(self):
        return hash(f"{self.row},{self.col}")


def is_digit(c: str) -> bool:
    try:
        int(c)
        return True
    except ValueError:
        return False


def read() -> Tuple[List[Part], List[str]]:
    with open("input.txt") as file:
        lines = [x.strip() for x in file.readlines()]
        parts = []

        for row, line in enumerate(lines):
            col = 0

            while col < len(line):
                c = line[col]
                if is_digit(c):  # Check for digits
                    j = col + 1
                    while j < len(line) and is_digit(line[j]):
                        j += 1

                    number = int(line[col:j])
                    parts.append(Part(number, row, col))
                    col = j
                else:  # Dot or symbol
                    col += 1

        return parts, lines


def part_is_valid(part: Part, schema: List[str]) -> bool:
    for row in range(part.row - 1, part.row + 2):
        for col in range(part.col - 1, part.col + len(str(part.number)) + 1):
            if 0 <= row < len(schema) and 0 <= col < len(schema[0]):
                char = schema[row][col]
                if not is_digit(char) and char != ".":  # Symbol found!
                    return True

    return False


def get_adjacent_parts(row: int, col: int, parts: List[Part], schema: List[str]) -> Set[Part]:
    adjacent_parts = set()

    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if 0 <= i < len(schema) and 0 <= j < len(schema[0]):
                for p in parts:
                    if i == p.row and p.col <= j < p.col + len(str(p.number)):
                        adjacent_parts.add(p)

    return adjacent_parts


def solve_snd(parts: List[Part], schema: List[str]) -> int:
    result = 0

    for row, line in enumerate(schema):
        for col, c in enumerate(line):
            if c == "*":  # Could be a gear
                adjacent_parts = get_adjacent_parts(row, col, parts, schema)

                if len(adjacent_parts) != 2:  # Not a gear!
                    continue

                adjacent_parts = list(adjacent_parts)
                gear_ratio = adjacent_parts[0].number * adjacent_parts[1].number

                result += gear_ratio

    return result


def main():
    parts, schema = read()
    parts = [p for p in parts if part_is_valid(p, schema)]
    print(f"First: {sum([p.number for p in parts])}")
    print(f"Second: {solve_snd(parts, schema)}")


if __name__ == "__main__":
    main()
