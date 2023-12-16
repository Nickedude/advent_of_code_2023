from itertools import combinations
from typing import Tuple, Set

import numpy as np


def read() -> np.ndarray:
    """Read the input into a binary numpy array."""
    with open("input.txt") as file:
        lines = [x.strip() for x in file.readlines()]
        height = len(lines)
        width = len(lines[0])
        image = np.zeros((height, width), dtype=int)

        for i, l in enumerate(lines):
            for j, c in enumerate(l):
                if c == "#":
                    image[i, j] = 1

        return image


def manhattan(neighbor: Tuple[int, int], goal: Tuple[int, int]) -> int:
    """Compute manhattan distance from neighbor to goal."""
    return abs(goal[0] - neighbor[0]) + abs(goal[1] - neighbor[1])


def get_distance(
    start: Tuple[int, int],
    goal: Tuple[int, int],
    empty_rows: Set[int],
    empty_cols: Set[int],
    expansion: int,
) -> int:
    """Get the distance from start to goal while accounting for the expansion of empty rows & cols."""
    distance = manhattan(start, goal)
    to_add = expansion - 1

    for row in range(min(start[0], goal[0]), max(start[0], goal[0]) + 1):
        if row in empty_rows:
            distance += to_add

    for col in range(min(start[1], goal[1]), max(start[1], goal[1]) + 1):
        if col in empty_cols:
            distance += to_add

    return distance


def get_empty_rows_and_cols(universe: np.ndarray) -> Tuple[Set[int], ...]:
    """Get empty rows and cols in the universe."""
    mask = universe == 0
    empty_rows = np.where(mask.all(axis=1))[0]
    empty_cols = np.where(mask.all(axis=0))[0]

    return set(empty_rows), set(empty_cols)


def sum_of_shortest_paths(
    universe: np.ndarray, empty_rows: Set[int], empty_cols: Set[int], expansion: int
) -> int:
    """Get the sum of shortest paths."""
    galaxies = np.stack(np.where(universe), axis=1)
    indices = list(range(len(galaxies)))
    pairs = list(combinations(indices, 2))
    sum_of_paths = 0

    for start, goal in pairs:
        sum_of_paths += get_distance(
            tuple(galaxies[start]),
            tuple(galaxies[goal]),
            empty_rows,
            empty_cols,
            expansion,
        )

    return sum_of_paths


def main():
    universe = read()
    empty_rows, empty_cols = get_empty_rows_and_cols(universe)
    print(sum_of_shortest_paths(universe, empty_rows, empty_cols, expansion=2))
    print(sum_of_shortest_paths(universe, empty_rows, empty_cols, expansion=1_000_000))


if __name__ == "__main__":
    main()
