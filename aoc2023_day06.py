"""
    Advent of Code 2023
    Day 06: Wait For It
"""

import re
from math import ceil, floor, prod, sqrt

import pytest


def parse_input(file_name: str) -> list[list[str]]:
    with open(file_name, "r", encoding="ascii") as data_file:
        return [re.findall(r"\d+", line) for line in data_file.read().splitlines()]


def solve(time: int, distance: int) -> tuple[int, int]:
    sd = sqrt((time**2) - 4 * distance)
    low = ceil((-sd + time) / 2)
    high = floor((sd + time) / 2)

    # must break the record, not just equal it
    if low * (time - low) == distance:
        low += 1
    if high * (time - high) == distance:
        high -= 1

    return low, high


def count_solutions(time: int, distance: int) -> int:
    low, high = solve(time, distance)
    return high - low + 1


def day06_part1(data: list[list[str]]) -> int:
    races = [
        (time, distance) for time, distance in zip(map(int, data[0]), map(int, data[1]))
    ]
    return prod(count_solutions(time, distance) for time, distance in races)


def day06_part2(data: list[list[str]]) -> int:
    time, distance = [int("".join(line)) for line in data]
    return count_solutions(time, distance)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day06_test.txt")


def test_day06_part1(test_data):
    assert day06_part1(test_data) == 288


def test_day06_part2(test_data):
    assert day06_part2(test_data) == 71503


if __name__ == "__main__":
    input_data = parse_input("data/day06.txt")

    print("Day 06 Part 1:")
    print(day06_part1(input_data))  # Correct answer is 293046

    print("Day 06 Part 2:")
    print(day06_part2(input_data))  # Correct answer is 35150181
