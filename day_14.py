from typing import Tuple, List

import numpy as np
from tqdm import tqdm

EMPTY = 0
ROUND_ROCK = 1
STEADY_ROCK = 2


def read() -> np.ndarray:
    with open("input.txt") as file:
        lines = [x.strip() for x in file.readlines()]
        world = []

        for line in lines:
            world.append([])

            for c in line:
                if c == ".":
                    world[-1].append(EMPTY)
                elif c == "#":
                    world[-1].append(STEADY_ROCK)
                elif c == "O":
                    world[-1].append(ROUND_ROCK)
                else:
                    raise ValueError()

            world[-1] = np.array(world[-1])

        return np.stack(world)


def tip_north(world: np.ndarray, indices: np.array) -> np.ndarray:
    new_world = world.copy()
    new_indices = np.zeros((len(indices), 2), dtype=int)

    for i in np.argsort(indices[:, 0]):
        row, col = indices[i]
        new_world[row, col] = EMPTY
        while True:
            if row - 1 >= 0 and new_world[row - 1, col] == EMPTY:
                row -= 1
            else:
                break

        new_world[row, col] = ROUND_ROCK
        new_indices[i] = [row, col]

    return new_world, new_indices


def tip_south(world: np.ndarray, indices: np.ndarray) -> np.ndarray:
    new_world = world.copy()
    new_indices = np.zeros((len(indices), 2), dtype=int)

    for i in np.argsort(indices[:, 0])[::-1]:
        row, col = indices[i]
        new_world[row, col] = EMPTY
        while True:
            if row + 1 < len(world) and new_world[row + 1, col] == EMPTY:
                row += 1
            else:
                break

        new_world[row, col] = ROUND_ROCK
        new_indices[i] = [row, col]

    return new_world, new_indices


def tip_west(world: np.ndarray, indices: np.ndarray) -> np.ndarray:
    new_world = world.copy()
    new_indices = np.zeros((len(indices), 2), dtype=int)

    for i in np.argsort(indices[:, 1]):
        [row, col] = indices[i]
        new_world[row, col] = EMPTY
        while True:
            if col - 1 >= 0 and new_world[row, col - 1] == EMPTY:
                col -= 1
            else:
                break

        new_world[row, col] = ROUND_ROCK
        new_indices[i] = [row, col]

    return new_world, new_indices


def tip_east(world: np.ndarray, indices: np.ndarray) -> np.ndarray:
    new_world = world.copy()
    new_indices = np.zeros((len(indices), 2), dtype=int)

    for i in np.argsort(indices[:, 1])[::-1]:
        row, col = indices[i]
        new_world[row, col] = EMPTY
        while True:
            if col + 1 < world.shape[1] and new_world[row, col + 1] == EMPTY:
                col += 1
            else:
                break

        new_world[row, col] = ROUND_ROCK
        new_indices[i] = [row, col]

    return new_world, new_indices


def cycle(world: np.ndarray, indices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    world, indices = tip_north(world, indices)
    world, indices = tip_west(world, indices)
    world, indices = tip_south(world, indices)
    world, indices = tip_east(world, indices)

    return world, indices


def detect_cycle(history: List[np.ndarray]) -> Tuple[int, int]:
    hare = 2
    tortoise = 1

    # Move the hare and the tortoise until they are equal
    while (history[hare] != history[tortoise]).any():
        hare += 2
        tortoise += 1

    # Find the first repetition of the cycle
    # At this point the tortoise position, v, is at a multiple of the cycle length
    # The tortoise position is also equal to the distance to the hare

    start = 0
    tortoise = 0

    # Move tortoise and hare forward at equal pace
    while (history[tortoise] != history[hare]).any():
        tortoise += 1
        hare += 1
        start += 1

    # Now the tortoise and hare both point to the same repeated value
    # We find the length of the shortest cycle starting from the first repeated value
    length = 1
    hare = tortoise + 1
    while (history[tortoise] != history[hare]).any():
        hare += 1
        length += 1

    return start, length


def run_cycles(world: np.ndarray, num_cycles: int) -> np.ndarray:
    rows, cols = np.where(world == ROUND_ROCK)
    indices = np.stack([rows, cols], axis=1, dtype=int)
    world_history = []

    for _ in tqdm(range(1000)):
        world, indices = cycle(world, indices)
        world_history.append(world)

    start, length = detect_cycle(world_history)
    print(f"Cycle start and length: ", start, length)

    cycles_remaining = num_cycles - (start + 1)
    idx = cycles_remaining % length
    return world_history[start + idx]


def compute_load(world: np.ndarray) -> int:
    load = 0

    for i in range(world.shape[0]):
        count = (world[i, :] == ROUND_ROCK).sum()
        weight = world.shape[0] - i
        load += count * weight

    return load


def print_world(world: np.ndarray):
    for i in range(world.shape[0]):
        for j in range(world.shape[1]):
            if world[i,j] == EMPTY:
                print(".", end="")
            elif world[i,j] == ROUND_ROCK:
                print("O", end="")
            elif world[i,j] == STEADY_ROCK:
                print("#", end="")

        print("")


def main():
    world = read()
    rows, cols = np.where(world == ROUND_ROCK)
    indices = np.stack([rows, cols], axis=1, dtype=int)
    tipped, _ = tip_north(world, indices)
    print(f"First answer: {compute_load(tipped)}")

    cycled = run_cycles(world, num_cycles=1_000_000_000)
    print(f"Second answer: {compute_load(cycled)}")


if __name__ == "__main__":
    main()
