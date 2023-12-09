from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from typing import Tuple, List, Dict
from enum import IntEnum

from tqdm import tqdm


class Instruction(IntEnum):
    Left = 0
    Right = 1


@dataclass
class Node:

    id_: str
    left: Node = None
    right: Node = None

    def __repr__(self):
        return f"{self.left.id_} <- {self.id_} -> {self.right.id_}"


def read() -> Tuple[Dict[str, Node], List[Instruction]]:
    with open("input.txt") as file:
        lines = [x.strip() for x in file.readlines()]

        instructions = lines[0]
        instructions = [
            Instruction.Left if i == "L" else Instruction.Right for i in instructions
        ]

        nodes = {}

        # Define all nodes without left/right pointers
        for line in lines[2:]:
            id_ = line.split(" = ")[0]
            nodes[id_] = Node(id_=id_)

        # Add left/right pointers to all nodes
        for line in lines[2:]:
            id_, neighbors = line.split(" = ")
            left, right = neighbors[1:-1].split(", ")

            left = nodes[left.strip()]
            right = nodes[right.strip()]
            nodes[id_].left = left
            nodes[id_].right = right

        for node in nodes.values():
            assert node.left is not None
            assert node.right is not None

        return nodes, instructions


def get_num_steps_to_goal_one_start(
    nodes: Dict[str, Node], instructions: List[Instruction]
):
    steps = 0
    at_goal = False
    current = nodes["AAA"]

    while not at_goal:
        for i in instructions:
            if current.id_ == "ZZZ":
                at_goal = True
                break

            steps += 1
            if i == Instruction.Left:
                current = current.left
            elif i == Instruction.Right:
                current = current.right
            else:
                raise ValueError()

    return steps


def get_primes(n: int) -> List[int]:
    primes = []
    remaining = n

    for i in range(2, n + 1):
        while remaining % i == 0:
            primes.append(i)
            remaining = remaining / i

    return primes


def get_num_steps_to_goal_multiple_starts(
    nodes: Dict[str, Node], instructions: List[Instruction]
):
    steps = 0
    iterations = 0
    starts = [node for id_, node in nodes.items() if id_[-1] == "A"]
    currents = deepcopy(starts)
    print(f"Num starts: {len(currents)}, {[c.id_ for c in currents]}")
    ends = dict()

    # For each start, find the step at which it reaches the goal
    # They'll reach the goal again and again with this periodicity
    while len(ends) != len(starts):
        for i in instructions:
            for j, c in enumerate(currents):
                if c.id_[-1] == "Z":
                    ends[(starts[j].id_, c.id_)] = steps

            steps += 1
            if i == Instruction.Left:
                currents = [c.left for c in currents]
            elif i == Instruction.Right:
                currents = [c.right for c in currents]
            else:
                raise ValueError()

        iterations += 1

    # Find the maximum number of steps
    # A multiple of this will be the answer
    max_ = max(ends.values())
    max_primes = get_primes(max_)

    for s in ends.values():
        if s != max_:
            for p in get_primes(s):
                if p not in max_primes:
                    max_primes.append(p)

    result = 1

    for p in max_primes:
        result *= p

    return result


def main():
    nodes, instructions = read()

    steps = get_num_steps_to_goal_one_start(nodes, instructions)
    print(f"Num steps: {steps}")

    steps = get_num_steps_to_goal_multiple_starts(nodes, instructions)
    print(f"Num steps: {steps}")


if __name__ == "__main__":
    main()
