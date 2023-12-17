from typing import List

import numpy as np


def read() -> List[np.ndarray]:
    with open("input.txt") as file:
        lines = [x.strip() for x in file.readlines()] + [""]
        current = []
        patterns = []

        for line in lines:
            if not line:
                current = np.stack(current)
                patterns.append(current)
                current = []
                continue

            digitized = np.zeros(len(line))
            for i, c in enumerate(line):
                if c == "#":
                    digitized[i] = 1.0

            current.append(digitized)

        return patterns


def get_column_count(pattern: np.ndarray, num_different: int) -> int:
    for col in range(0, pattern.shape[1] - 1):
        # Check for reflection starting between col and col+1
        has_reflection = True
        local_num_different = 0

        for distance in range(0, pattern.shape[1]):
            left = col - distance
            right = col + distance + 1

            if left < 0 or right >= pattern.shape[1]:
                break

            diff = (pattern[:, left] != pattern[:, right]).sum()
            local_num_different += diff
            if local_num_different > num_different:
                has_reflection = False
                break

        if has_reflection and local_num_different == num_different:
            return col + 1

    return 0


def get_row_count(pattern: np.ndarray, num_different: int) -> int:
    for row in range(0, pattern.shape[0] - 1):
        # Check for reflection starting between row and row+1
        has_reflection = True
        local_num_different = 0

        for distance in range(0, pattern.shape[0]):
            up = row - distance
            down = row + distance + 1

            if up < 0 or down >= pattern.shape[0]:
                break

            diff = (pattern[up, :] != pattern[down, :]).sum()
            local_num_different += diff
            if local_num_different > num_different:
                has_reflection = False
                break

        if has_reflection and local_num_different == num_different:
            return row + 1

    return 0


def solve(patterns: List[np.ndarray], num_different: int = 0) -> int:
    count = 0

    for pattern in patterns:
        num_columns = get_column_count(pattern, num_different)

        if num_columns > 0:
            count += num_columns
        else:
            count += 100 * get_row_count(pattern, num_different)

    return count


def main():
    patterns = read()
    print(f"First answer: {solve(patterns)}")
    print(f"First answer: {solve(patterns, num_different=1)}")


if __name__ == "__main__":
    main()
