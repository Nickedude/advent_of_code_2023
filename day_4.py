from dataclasses import dataclass
from typing import Set, List


@dataclass
class ScratchCard:

    id_: str
    winning: Set[int]
    content: Set[int]

    def get_num_wins(self) -> int:
        return len(self.winning.intersection(self.content))

    def get_points(self) -> int:
        num_wins = self.get_num_wins()

        if num_wins == 0:
            return 0

        return 2 ** (num_wins - 1)


def parse_numbers(s: str) -> List[int]:
    s = s.strip()
    xs = s.split(" ")
    xs = [x for x in xs if x]
    return list(map(int, xs))


def read() -> List[ScratchCard]:
    with open("input.txt") as file:
        lines = [line.strip() for line in file.readlines()]
        cards = []

        for line in lines:
            id_, numbers = line.split(":")
            winning, content = numbers.split(" | ")
            winning = parse_numbers(winning)
            content = parse_numbers(content)

            cards.append(ScratchCard(id_, set(winning), set(content)))

        return cards


def get_total_points(cards: List[ScratchCard]) -> int:
    return sum([c.get_points() for c in cards])


def get_total_number_of_scratchcards(cards: List[ScratchCard]) -> int:
    cards = sorted(cards, key=lambda c: c.id_)
    card_count = {c.id_: 1 for c in cards}

    for i, c in enumerate(cards):
        num_wins = c.get_num_wins()

        for j in range(i + 1, i + num_wins + 1):
            card_count[cards[j].id_] += card_count[c.id_]

    num_cards = sum(list(card_count.values()))

    return num_cards


def main():
    cards = read()
    print(f"First: {get_total_points(cards)}")
    print(f"First: {get_total_number_of_scratchcards(cards)}")


if __name__ == "__main__":
    main()
