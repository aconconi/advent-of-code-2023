"""
    Advent of Code 2023
    Day 08: Haunted Wasteland
"""

from itertools import count, cycle
from math import lcm
from typing import Callable

import pytest


def parse_input(file_name: str) -> tuple[str, dict[str, tuple[str, str]]]:
    with open(file_name, "r", encoding="ascii") as data_file:
        directions, _, *nodes = data_file.read().splitlines()
    return directions, {line[:3]: (line[7:10], line[12:15]) for line in nodes}


def solve(
    directions: str, start: str, nodes: dict[str, tuple[str, str]], is_exit: Callable
) -> int:
    current = start
    ans = 0
    for direction, step in zip(cycle(directions), count(start=1)):
        current = nodes[current][0 if direction == "L" else 1]
        if is_exit(current):
            ans = step
            break
    return ans


def day08_part1(data: tuple[str, dict[str, tuple[str, str]]]) -> int:
    directions, nodes = data
    return solve(directions, "AAA", nodes, is_exit=lambda node: node == "ZZZ")


def day08_part2(data: tuple[str, dict[str, tuple[str, str]]]) -> int:
    directions, nodes = data
    solutions = [
        solve(directions, start_node, nodes, is_exit=lambda node: node[-1] == "Z")
        for start_node in nodes
        if start_node[-1] == "A"
    ]
    return lcm(*solutions)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return [parse_input("data/day08_test1.txt"), parse_input("data/day08_test2.txt")]


def test_day08_part1(test_data):
    assert day08_part1(test_data[0]) == 2


def test_day08_part2(test_data):
    assert day08_part2(test_data[1]) == 6


if __name__ == "__main__":
    input_data = parse_input("data/day08.txt")

    print("Day 08 Part 1:")
    print(day08_part1(input_data))

    print("Day 08 Part 2:")
    print(day08_part2(input_data))
