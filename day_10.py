from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple

from tqdm import tqdm


class TileType(Enum):

    Vertical = "|"
    Horizontal = "-"
    NorthEast = "L"
    NorthWest = "J"
    SouthEast = "F"
    SouthWest = "7"
    Ground = "."
    Start = "S"

    @classmethod
    def from_character(cls, c: str) -> TileType:
        for type_ in cls:
            if type_.value == c:
                return type_


@dataclass
class Node:

    # Type of node
    type_: TileType

    # Next nodes in clockwise order
    forward: Node = None
    backward: Node = None


def read() -> List[List[TileType]]:
    with open("input.txt") as file:
        lines = [x.strip() for x in file.readlines()]

        graph = []

        for line in lines:
            row = []

            for c in line:
                type_ = TileType.from_character(c)
                row.append(type_)

            graph.append(row)

        return graph


def get_neighbors(
    row: int, col: int, graph: List[List[TileType]]
) -> List[Tuple[int, int]]:
    current = graph[row][col]

    if current == TileType.Vertical:
        return [(row - 1, col), (row + 1, col)]
    elif current == TileType.Horizontal:
        return [(row, col + 1), (row, col - 1)]
    elif current == TileType.NorthEast:
        return [(row - 1, col), (row, col + 1)]
    elif current == TileType.NorthWest:
        return [(row - 1, col), (row, col - 1)]
    elif current == TileType.SouthEast:
        return [(row + 1, col), (row, col + 1)]
    elif current == TileType.SouthWest:
        return [(row + 1, col), (row, col - 1)]
    elif current == TileType.Ground:
        # Stop if we end up on bare ground
        return []
    else:
        raise ValueError(f"Unknown tile: {current}")


def is_traversable(
    current: Tuple[int, int],
    neighbor: Tuple[int, int],
    graph: List[List[TileType]],
) -> bool:
    row, col = current
    neighbor_row, neighbor_col = neighbor
    neighbor_type = graph[neighbor_row][neighbor_col]

    if graph[neighbor_row][neighbor_col] == TileType.Ground:
        return False

    # Find the direction we're moving in
    row_dir = neighbor_row - row
    col_dir = neighbor_col - col

    if row_dir == 0:  # Horizontally
        if col_dir > 0:  # West to east
            # New pipe can be one of these
            return neighbor_type in [TileType.Horizontal, TileType.NorthWest, TileType.SouthWest]
        else:  # East to west
            return neighbor_type in [TileType.Horizontal, TileType.NorthEast, TileType.SouthEast]
    elif col_dir == 0:  # Laterally
        if row_dir > 0:  # North to south
            return neighbor_type in [TileType.Vertical, TileType.NorthEast, TileType.NorthWest]
        else:  # South to north
            return neighbor_type in [TileType.Vertical, TileType.SouthEast, TileType.SouthWest]

    return False


def dfs(row_start: int, col_start: int, graph: List[List[TileType]]) -> List[Tuple[int, int]]:
    # Do a DFS until the loop is closed or the path ends
    visited = set()
    queue = [((row_start, col_start), [])]
    # predecessor_map = {}

    while len(queue) > 0:
        current, path = queue.pop(-1)

        if current in visited:
            continue

        predecessor = None if len(path) == 0 else path[-1]
        row, col = current

        # Check if we're at the goal
        if row == row_start and col == col_start:
            # We've reached the goal if the path has non-zero length
            # If not, this is the first iteration of the search
            if len(path) > 0:
                # path = [current]
                # while predecessor != current:
                #     path.append(predecessor)
                #     predecessor = predecessor_map[predecessor]
                return path
        # If not, mark the node as visited
        else:
            visited.add((row, col))

        for neighbor in get_neighbors(row, col, graph):
            if neighbor == predecessor or neighbor in visited:
                continue

            neighbor_row, neighbor_col = neighbor

            # Check if new row out of bounds
            if neighbor_row < 0 or neighbor_row >= len(graph):
                continue

            # Check if new col out of bounds
            if neighbor_col < 0 or neighbor_col >= len(graph[0]):
                continue

            # Check if neighbor traversable from our location
            if is_traversable(current, neighbor, graph):
                new_path = deepcopy(path)
                new_path.append(current)
                queue.append((neighbor, new_path))

    # Search ended without reaching goal
    return []


def get_loop(graph: List[List[TileType]]) -> List[Tuple[int, int]]:
    # Find start node:
    row_start, col_start = 0, 0

    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j] == TileType.Start:
                row_start = i
                col_start = j

    # Check which type of pipe that yields a loop
    for type_ in TileType:
        if type_ in (TileType.Ground, TileType.Start):
            continue

        graph[row_start][col_start] = type_
        path = dfs(row_start, col_start, graph)

        if len(path) > 0:
            return path


def get_num_tiles_in_loop(loop: List[Tuple[int, int]], graph: List[List[TileType]]) -> int:
    # Consider the loop as a polygon - try to find all points inside the polygon
    loop_nodes = set(loop)

    # Form the edges of the polygon by finding all "corners"
    edges = [loop[0]]

    for i in range(1, len(loop)):
        current = loop[i]
        last_corner = edges[-1]

        if not(current[0] == last_corner[0] or current[1] == last_corner[1]):  # On the same row/col:
            edges.append(loop[i-1])

    # for i in range(len(graph)):
    #     for j in range(len(graph[0])):
    #         if any((i, j) in e for e in edges):
    #             print("O", end="")
    #         else:
    #             print(".", end="")
    #
    #     print("")

    num_tiles_inside = 0

    for i in tqdm(range(len(graph))):
        for j in range(len(graph[i])):
            # A loop node is not inside the loop
            if (i, j) in loop_nodes:
                continue

            # Count the number of times a ray from this tile will intersect the polygon
            intersecting = set()

            for ray in range(i, len(graph)):
                for e in range(len(edges)):
                    start = edges[e]
                    stop = edges[(e + 1) % len(edges)]

                    # Ray shoots up to down, ignore all edges that are vertical
                    if start[1] == stop[1]:
                        continue

                    cols = sorted([start[1], stop[1]])
                    rows = sorted([start[0], stop[0]])

                    if cols[0] <= j <= cols[1] and ray == rows[0]:  # Ray col overlaps with edge and ray row hits edge
                        intersecting.add((start, stop))

            if len(intersecting) % 2 != 0:
                num_tiles_inside += 1
                print(i, j, [sorted(list(i)) for i in intersecting])

    return num_tiles_inside


def main():
    graph = read()
    path = get_loop(graph)
    print(f"First answer: {len(path) // 2}")
    print(f"Second answer: {get_num_tiles_in_loop(path, graph)}")


if __name__ == "__main__":
    main()
