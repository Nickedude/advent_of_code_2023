from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, Dict, Set
from enum import Enum

from tqdm import tqdm


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


MIRROR_LEFT_TRANSITION = {
    Direction.UP: Direction.LEFT,
    Direction.DOWN: Direction.RIGHT,
    Direction.LEFT: Direction.UP,
    Direction.RIGHT: Direction.DOWN,
}

MIRROR_RIGHT_TRANSITION = {
    Direction.UP: Direction.RIGHT,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.DOWN,
    Direction.RIGHT: Direction.UP,
}


class TileType(Enum):
    EMPTY = "."
    SPLITTER_VERTICAL = "|"
    SPLITTER_HORIZONTAL = "-"
    MIRROR_RIGHT = "/"
    MIRROR_LEFT = "\\"

    @classmethod
    def from_character(cls, c: str) -> TileType:
        for type_ in cls:
            if type_.value == c:
                return type_


@dataclass
class Node:
    row: int
    col: int
    type_: TileType
    up: Node = None
    down: Node = None
    left: Node = None
    right: Node = None

    def __hash__(self):
        return hash((self.row, self.col))


def read() -> Dict[Tuple[int, int]]:
    with open("input.txt") as file:
        lines = [x.strip() for x in file.readlines()]
        graph = {}

        for row, line in enumerate(lines):
            for col, c in enumerate(line):
                graph[(row, col)] = Node(row, col, TileType.from_character(c))

        for row in range(len(lines)):
            for col in range(len(lines[0])):
                node = graph[(row, col)]

                if (row - 1) >= 0:
                    node.up = graph[(row - 1, col)]
                if (row + 1) < len(lines):
                    node.down = graph[(row + 1, col)]
                if (col - 1) >= 0:
                    node.left = graph[(row, col - 1)]
                if (col + 1) < len(lines[0]):
                    node.right = graph[(row, col + 1)]

        return graph


def get_energized_nodes(
    graph: Dict[Tuple[int, int], Node],
    start: Tuple[int, int, Direction],
) -> Set[Tuple[int, int]]:
    """Do a BFS to get all visited nodes."""
    visited = set()
    queue = [(graph[(start[0], start[1])], start[2])]

    while len(queue) > 0:
        next_element = queue.pop(0)

        if next_element in visited:
            continue
        else:
            visited.add(next_element)

        current, direction = next_element

        neighbors = []

        if current.type_ == TileType.EMPTY:
            neighbors.append((getattr(current, direction.value), direction))
        elif current.type_ == TileType.MIRROR_LEFT:
            new_direction = MIRROR_LEFT_TRANSITION[direction]
            neighbors.append((getattr(current, new_direction.value), new_direction))
        elif current.type_ == TileType.MIRROR_RIGHT:
            new_direction = MIRROR_RIGHT_TRANSITION[direction]
            neighbors.append((getattr(current, new_direction.value), new_direction))
        elif current.type_ == TileType.SPLITTER_VERTICAL:
            if direction in [Direction.UP, Direction.DOWN]:
                neighbors.append((getattr(current, direction.value), direction))
            else:
                neighbors.append((current.up, Direction.UP))
                neighbors.append((current.down, Direction.DOWN))
        elif current.type_ == TileType.SPLITTER_HORIZONTAL:
            if direction in [Direction.RIGHT, Direction.LEFT]:
                neighbors.append((getattr(current, direction.value), direction))
            else:
                neighbors.append((current.left, Direction.LEFT))
                neighbors.append((current.right, Direction.RIGHT))
        else:
            raise ValueError()

        for n in neighbors:
            if n[0] and n not in visited:
                queue.append(n)

    indices = set([(n.row, n.col) for n, _ in visited])
    return indices


def print_visited(indices: Set[Tuple[int, int]], graph: Dict[Tuple[int, int], Node]):
    for i in range(get_height(graph)):
        for j in range(get_width(graph)):
            if (i, j) in indices:
                print("#", end="")
            else:
                print(".", end="")
        print("")


def get_width(graph: Dict[Tuple[int, int], Node]) -> int:
    return max(n.col + 1 for n in graph.values())


def get_height(graph: Dict[Tuple[int, int], Node]) -> int:
    return max(n.row + 1 for n in graph.values())


def main():
    graph = read()
    visited = get_energized_nodes(graph, (0, 0, Direction.RIGHT))
    print(f"First answer: {len(visited)}")

    max_visited = 0
    width = get_width(graph)
    height = get_height(graph)

    for row in tqdm(range(height)):
        max_visited = max(
            max_visited, len(get_energized_nodes(graph, (row, 0, Direction.RIGHT)))
        )
        max_visited = max(
            max_visited,
            len(get_energized_nodes(graph, (row, width - 1, Direction.LEFT))),
        )

    for col in tqdm(range(width)):
        max_visited = max(
            max_visited, len(get_energized_nodes(graph, (0, col, Direction.DOWN)))
        )
        max_visited = max(
            max_visited,
            len(get_energized_nodes(graph, (height - 1, col, Direction.UP))),
        )

    print(f"Second answer: {max_visited}")


if __name__ == "__main__":
    main()
