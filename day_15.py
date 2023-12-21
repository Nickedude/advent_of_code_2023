from typing import List, Tuple

from tqdm import tqdm


def read() -> List[str]:
    with open("input.txt") as file:
        line = file.readlines()[0].strip()
        return line.split(",")


def my_hash(s: str) -> int:
    current = 0

    for c in s:
        current += ord(c)
        current *= 17
        current = current % 256

    return current


def get_lens_idx(box: List[Tuple[str, int]], label: str) -> int:
    lens_idx = -1
    for i, (existing_label, _) in enumerate(box):
        if existing_label == label:
            lens_idx = i
            break

    return lens_idx


def run_initialization_sequence(initialization_sequence: List[str]):
    boxes = [list() for _ in range(256)]

    for seq in initialization_sequence:

        if "=" in seq:
            label, focal_length = seq.split("=")
            focal_length = int(focal_length)
            box_idx = my_hash(label)
            lens_idx = get_lens_idx(boxes[box_idx], label)

            if lens_idx >= 0:
                boxes[box_idx][lens_idx] = label, focal_length
            else:
                boxes[box_idx].append((label, focal_length))

        elif "-" in seq:
            label = seq.split("-")[0]
            box_idx = my_hash(label)
            lens_idx = get_lens_idx(boxes[box_idx], label)

            if lens_idx >= 0:
                boxes[box_idx].pop(lens_idx)

        else:
            raise ValueError()

    return boxes


def get_focusing_power(boxes: List[List[Tuple[str, int]]]):
    focusing_power = 0

    for i, b in enumerate(boxes):
        for j, (_, f) in enumerate(b):
            focusing_power += (i + 1) * (j + 1) * f

    return focusing_power


def main():
    initialization_sequence = read()
    print(f"First answer: {sum(map(my_hash, tqdm(read())))}")
    boxes = run_initialization_sequence(initialization_sequence)
    print(f"Second answer: {get_focusing_power(boxes)}")


if __name__ == "__main__":
    main()
