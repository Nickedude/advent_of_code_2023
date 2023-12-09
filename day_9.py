from typing import List, Tuple
import numpy as np


def read() -> List[np.ndarray]:
    with open("input.txt") as file:
        lines = [x.strip() for x in file.readlines()]
        lines = [line.split(" ") for line in lines]
        return [np.array([int(c) for c in line]) for line in lines]


def extrapolate_helper(sequence: np.ndarray, idx: int, sign: int) -> int:
    if (sequence == 0).all():
        return 0

    next_sequence = sequence[1:] - sequence[:-1]
    below = extrapolate_helper(next_sequence, idx, sign)
    return sequence[idx] + sign * below


def extrapolate_forward(sequence: np.ndarray):
    return extrapolate_helper(sequence, idx=-1, sign=1)


def extrapolate_backward(sequence: np.ndarray) -> int:
    return extrapolate_helper(sequence, idx=0, sign=-1)


def get_sums_of_extrapolated_values(sequences: List[np.ndarray]) -> Tuple[int, int]:
    forward_sum = 0
    backward_sum = 0

    for s in sequences:
        forward_sum += extrapolate_forward(s)
        backward_sum += extrapolate_backward(s)

    return forward_sum, backward_sum


def main():
    nums = read()
    print(f"Answers: {get_sums_of_extrapolated_values(nums)}")


if __name__ == "__main__":
    main()
