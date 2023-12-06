import math
from typing import List, Tuple


def parse_line(line: str) -> List[int]:
    line = line.split(":")[1]
    numbers = []

    for i in line.split(" "):
        i = i.strip()

        if not i:
            continue

        numbers.append(int(i))

    return numbers


def read() -> Tuple[List[int], List[int]]:
    with open("input.txt") as file:
        lines = [x.strip() for x in file.readlines()]
        times = lines[0]
        distances = lines[1]

        return parse_line(times), parse_line(distances)


def get_min_velocity(distance: int, time: int) -> int:
    return math.floor(distance / time)


def get_travelled_distance(velocity: int, max_time: int) -> int:
    remaining = max_time - velocity
    return velocity * remaining


def solve_fst(times: List[int], distances: List[int]) -> int:
    result = 1

    for max_time, best_distance in zip(times, distances):
        num_win_alternatives = 0
        min_velocity = get_min_velocity(best_distance, max_time)

        for velocity in range(min_velocity, max_time + 1):
            if get_travelled_distance(velocity, max_time) > best_distance:
                num_win_alternatives += 1

        result *= num_win_alternatives

    return result


def joint_ints(ints: List[int]) -> int:
    return int("".join([str(i) for i in ints]))


def solve_snd(times: List[int], distances: List[int]) -> int:
    time = joint_ints(times)
    best_distance = joint_ints(distances)

    num_win_alternatives = 0
    min_velocity = get_min_velocity(best_distance, time)

    for velocity in range(min_velocity, time + 1):
        if get_travelled_distance(velocity, time) > best_distance:
            num_win_alternatives += 1

    return num_win_alternatives


def main():
    times, distances = read()
    print(f"First: {solve_fst(times, distances)}")
    print(f"Second: {solve_snd(times, distances)}")


if __name__ == "__main__":
    main()
