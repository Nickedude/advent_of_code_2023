from typing import List

STRING_TO_DIGIT = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def read() -> List[str]:
    with open("input.txt") as file:
        return [x.strip() for x in file.readlines()]


def solve(input_: List[str], consider_strings: bool = False) -> int:
    result = 0

    for line in input_:
        first, last = None, None
        for i, c in enumerate(line):
            digit = None
            try:
                int(c)
                digit = c
            except ValueError:
                pass

            if digit is None and consider_strings:
                for s, d in STRING_TO_DIGIT.items():
                    if line[i : i + len(s)] == s:
                        digit = str(d)
                        break

            if digit is not None:
                first = digit if first is None else first
                last = digit

        result += int(first + last)

    return result


def main():
    input_ = read()
    print(f"First: {solve(input_)}")
    print(f"Second: {solve(input_, consider_strings=True)}")


if __name__ == "__main__":
    main()
