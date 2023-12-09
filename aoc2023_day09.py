"""
    Advent of Code 2023
    Day 09: Mirage Maintenance
"""

from itertools import pairwise

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return [
            [int(x) for x in line.split()] for line in data_file.read().splitlines()
        ]


def extrapolate(seq: list[int], backwards: bool=False) -> int:
    if all(x == 0 for x in seq):
        return 0
    idx, sgn = (0, -1) if backwards else (-1, +1)
    next_seq = [b - a for a, b in pairwise(seq)]
    return seq[idx] + sgn * extrapolate(next_seq, backwards)


def day09_part1(data):
    return sum(extrapolate(seq) for seq in data)


def day09_part2(data):
    return sum(extrapolate(seq, backwards=True) for seq in data)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day09_test.txt")


def test_day09_part1(test_data):
    assert day09_part1(test_data) == 114


def test_day09_part2(test_data):
    assert day09_part2(test_data) == 2


if __name__ == "__main__":
    input_data = parse_input("data/day09.txt")

    print("Day 09 Part 1:")
    print(day09_part1(input_data))  # Correct answer is 1806615041

    print("Day 09 Part 2:")
    print(day09_part2(input_data))  # Correct answer is 1211
