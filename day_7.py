from collections import defaultdict
from functools import cached_property
from typing import List, Dict, Union
from enum import IntEnum
from dataclasses import dataclass


class Type(IntEnum):
    FiveOfAKind = 1
    FourOfAKind = 2
    FullHouse = 3
    ThreeOfAKind = 4
    TwoPairs = 5
    OnePair = 6
    HighCard = 7

    @staticmethod
    def from_cards(cards: List[str]) -> "Type":
        count = defaultdict(int)

        for c in cards:
            count[c] += 1

        num_pairs = sum([c == 2 for c in count.values()])

        if len(count) == 1:  # All cards are the same
            return Type.FiveOfAKind
        elif any([c == 4 for c in count.values()]):
            return Type.FourOfAKind
        elif all([c == 2 or c == 3 for c in count.values()]):
            return Type.FullHouse
        elif any([c == 3 for c in count.values()]):
            return Type.ThreeOfAKind
        elif num_pairs == 2:
            return Type.TwoPairs
        elif num_pairs == 1:
            return Type.OnePair
        elif len(count) == 5:
            return Type.HighCard
        else:
            raise ValueError(f"Unknown type for hand: {cards}")

    @staticmethod
    def from_cards_with_joker(cards: List[str]) -> "Type":
        if "J" not in cards or all([c == "J" for c in cards]):
            return Type.from_cards(cards)

        # This set of cards has both jokers and other cards in it
        count = defaultdict(int)

        # Count cards of each kind
        for c in cards:
            count[c] += 1

        # All kinds of non-joker cards
        kinds = list([k for k in count.keys() if k != "J"])

        if len(count) == 2:
            # There's one regular kind of card + jokers
            return Type.FiveOfAKind
        elif len(count) == 3 and any(
            [(i + count["J"]) == 4 for c, i in count.items() if c != "J"]
        ):
            # There's two regular kinds of cards + jokers
            # We end up here if adding all jokers to one of the regular cards yields four
            return Type.FourOfAKind
        elif (
            len(count)
            == 3
            # and (count[kinds[1]] + count["J"] == 3 and count[kinds[0]] == 2)
            # or (count[kinds[0]] + count["J"] == 3 and count[kinds[1]] == 2)
        ):
            # There's two regular kinds of cards + jokers
            # We end up here if adding the jokers to one or the other adds a full house
            return Type.FullHouse
        elif len(count) == 4:
            # We end up here if we have three regular kinds of cards + jokers
            # This can either be:
            #   - three unique cards + two jokers, or
            #   - two unique cards, one pair and one joker
            # In both cases we can form three of a kind.
            return Type.ThreeOfAKind
        elif len(count) == 5:
            # We end up here if we have four kinds of real cards + a joker
            # Then we can always form a pair
            return Type.OnePair
        else:
            raise ValueError(f"Unknown type for hand: {cards}")


@dataclass
class Hand:
    bid: int
    type: Type
    cards: List[str]

    def __lt__(self, other):
        if self.type != other.type:
            return self.type < other.type

        for c1, c2 in zip(self.cards, other.cards):
            if c1 != c2:
                return self.order[c1] < self.order[c2]

        raise ValueError("Tie!")

    @cached_property
    def order(self) -> Dict[str, int]:
        return {c: i for i, c in enumerate(self.card_order)}

    @cached_property
    def card_order(self) -> List[str]:
        return ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]


@dataclass
class JokerHand(Hand):

    bid: int
    type: Type
    cards: List[str]

    @staticmethod
    def from_hand(hand: Hand) -> "JokerHand":
        return JokerHand(
            bid=hand.bid, type=Type.from_cards_with_joker(hand.cards), cards=hand.cards
        )

    @cached_property
    def card_order(self):
        return ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


def read() -> List[Hand]:
    with open("input.txt") as file:
        lines = [x.strip() for x in file.readlines()]
        hands = []

        for line in lines:
            hand, bid = line.split(" ")
            cards = [c for c in hand]
            bid = int(bid.strip())
            type_ = Type.from_cards(cards)
            hands.append(Hand(bid, type_, cards))

    return hands


def get_winnings(hands: List[Hand]) -> int:
    hands = sorted(hands)

    winnings = 0

    for i, h in enumerate(hands):
        rank = len(hands) - i
        winnings += rank * h.bid

    return winnings


def main():
    hands = read()
    print(f"Winnings: {get_winnings(hands)}")
    hands = [JokerHand.from_hand(h) for h in hands]
    print(f"Winnings: {get_winnings(hands)}")


if __name__ == "__main__":
    main()
