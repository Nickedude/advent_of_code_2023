from typing import List, Tuple, Dict
from tqdm import tqdm


def read() -> List[Tuple[str, List[int]]]:
    with open("input.txt") as file:
        lines = [x.strip() for x in file.readlines()]
        springs_and_counts = []

        for line in lines:
            springs, counts = line.split(" ")
            counts = [int(c) for c in counts.split(",")]
            springs_and_counts.append((springs, counts))

        return springs_and_counts


def simplify(springs: str) -> str:
    new = []

    # ...#.... -> .#.
    # #...# -> #.#

    for i, c in enumerate(springs):
        if springs[i] == ".":
            if i > 0 and springs[i-1] == ".":
                continue
            else:
                new.append(c)
        else:
            new.append(c)

    return "".join(new)


def get_actual_counts(springs: str) -> List[int]:
    current = 0
    actual_counts = []

    for c in springs:
        if c == "." and current > 0:
            actual_counts.append(current)
            current = 0
        if c == "#":
            current += 1

    if current > 0:
        actual_counts.append(current)

    return actual_counts


def is_valid(springs: str, counts: List[int]) -> bool:
    return get_actual_counts(springs) == counts


def get_valid_arrangements(springs: str, counts: List[int], memory: Dict) -> int:
    springs = simplify(springs)

    if springs not in memory:
        # If no unknowns remain, there are no more alternatives
        if "?" not in springs:
            if is_valid(springs, counts):
                return 1
            else:
                return 0

        arrangements = 0
        idx = springs.index("?")

        # Check if the arrangement is invalid
        counts_this_far = get_actual_counts(springs[:idx])

        if len(counts_this_far) > 0:
            # All groups observed except for the last one must be valid
            if counts_this_far[:-1] != counts[:len(counts_this_far) - 1]:
                return 0
            # The last observed group cannot be larger than it's match
            # If there are more groups observed than actual groups, match to the last one
            if counts_this_far[-1] > counts[min(len(counts_this_far) - 1, len(counts) - 1)]:
                return 0

        for alternative in [".", "#"]:
            springs_alt = springs[:idx] + alternative + springs[idx+1:]
            springs_alt = simplify(springs_alt)
            arrangements += get_valid_arrangements(springs_alt, counts, memory)

        memory[springs] = arrangements

    return memory[springs]


def get_num_valid_arrangements(springs_and_counts: List[Tuple[str, List[int]]]) -> int:
    count = 0

    for springs, counts in tqdm(springs_and_counts):
        count += get_valid_arrangements(simplify(springs), counts, memory={})

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
