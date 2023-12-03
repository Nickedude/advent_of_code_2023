from dataclasses import dataclass, fields
from typing import List


@dataclass
class CubeSet:
    red: int = 0
    blue: int = 0
    green: int = 0

    def power(self) -> int:
        return self.red * self.blue * self.green


@dataclass
class Game:
    id_: int
    subsets: List[CubeSet]


def read():
    with open("input.txt") as file:
        lines = [x.strip() for x in file.readlines()]
        games = []

        for line in lines:
            line = line.split("Game ")[1]
            id_, tail = line.split(": ")
            subsets = []
            for subset_string in tail.split("; "):
                subset = CubeSet()

                for element in subset_string.split(", "):
                    count, color = element.split(" ")
                    count = int(count)
                    setattr(subset, color, count)

                subsets.append(subset)

            games.append(Game(int(id_), subsets))

        return games


def subset_is_possible(subset: CubeSet) -> bool:
    maximum = CubeSet(red=12, blue=14, green=13)
    return (
        subset.red <= maximum.red
        and subset.blue <= maximum.blue
        and subset.green <= maximum.green
    )


def game_is_possible(game: Game) -> bool:
    for subset in game.subsets:
        if not subset_is_possible(subset):
            return False

    return True


def solve_fst(games: List[Game]) -> int:
    result = 0

    for game in games:
        if game_is_possible(game):
            result += game.id_

    return result


def get_minimum_subset(game: Game) -> CubeSet:
    minimum = CubeSet()

    for subset in game.subsets:
        for color in fields(minimum):
            x = getattr(subset, color.name)
            y = getattr(minimum, color.name)
            if x > y:
                setattr(minimum, color.name, x)

    return minimum


def solve_snd(games: List[Game]):
    result = 0

    for game in games:
        minimum = get_minimum_subset(game)
        result += minimum.power()

    return result


def main():
    games = read()
    print(f"First: {solve_fst(games)}")
    print(f"Second: {solve_snd(games)}")


if __name__ == "__main__":
    main()
