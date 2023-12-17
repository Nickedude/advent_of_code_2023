from functools import lru_cache
from typing import List, Tuple, Dict
from tqdm import tqdm


def read() -> List[Tuple[str, Tuple[int, ...]]]:
    with open("input.txt") as file:
        lines = [x.strip() for x in file.readlines()]
        springs_and_counts = []

        for line in lines:
            springs, counts = line.split(" ")
            counts = tuple([int(c) for c in counts.split(",")])
            springs_and_counts.append((springs, counts))

        return springs_and_counts


@lru_cache(maxsize=10000)
def get_valid_arrangements(springs: str, counts: Tuple[int, ...]) -> int:
    # Check if we're out of springs
    if not springs:
        # This case is valid if we're out of groups
        return 1 if len(counts) == 0 else 0

    # Check if we're out of groups
    if not counts:
        # This case is valid if we're out of damaged springs
        return 0 if "#" in springs else 1

    # Skip dots
    if springs[0] == ".":
        return get_valid_arrangements(springs[1:], counts)

    # If it's a damaged spring, match it to the next group
    elif springs[0] == "#":
        current = counts[0]

        # Check if the group can be fulfilled

        # The group cannot exceed the number of springs
        if current > len(springs):
            return 0

        # Nothing in the group can be empty
        for i in range(current):
            if springs[i] == ".":
                return 0

        # A new group can't start directly after this one
        if current < len(springs) and springs[current] == "#":
            return 0

        # If it can -> move on to beyond this group + one space
        return get_valid_arrangements(springs[current+1:], counts[1:])

    # If it's unknown -> investigate both options
    elif springs[0] == "?":
        empty_opt = get_valid_arrangements("." + springs[1:], counts)
        damaged_opt = get_valid_arrangements("#" + springs[1:], counts)
        return empty_opt + damaged_opt


def get_num_valid_arrangements(springs_and_counts: List[Tuple[str, Tuple[int, ...]]]) -> int:
    count = 0

    for springs, counts in tqdm(springs_and_counts):
        count += get_valid_arrangements(springs, counts)

    return count


def unfold(spring: str, counts: List[int]) -> Tuple[str, List[int]]:
    new_counts = counts * 5
    new_springs = "?".join([spring] * 5)
    return new_springs, new_counts


def main():
    springs_and_counts = read()
    print(f"First answer: {get_num_valid_arrangements(springs_and_counts)}")
    springs_and_counts = [unfold(*x) for x in springs_and_counts]
    print(f"Second answer: {get_num_valid_arrangements(springs_and_counts)}")


if __name__ == "__main__":
    main()
