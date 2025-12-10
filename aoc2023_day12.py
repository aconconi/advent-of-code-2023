"""
    Advent of Code 2023
    Day 12: Hot Springs
"""

from functools import cache

import pytest


def parse_input(file_name):
    def parse_line(line):
        line = line.split()
        return line[0], tuple(map(int, line[1].split(",")))

    with open(file_name, "r", encoding="ascii") as data_file:
        return [parse_line(line) for line in data_file.read().splitlines()]


@cache
def count_possible(seq: str, sizes: tuple[int]) -> int:
    if len(sizes) == 0:
        return 1 if seq.count("#") == 0 else 0

    max_size = max(sizes)
    idx_max_size = sizes.index(max_size)
    num_solutions = 0
    for i in range(len(seq) - max_size + 1):
        if (
            seq[i : i + max_size].count(".") == 0
            and (i == 0 or seq[i - 1] != "#")
            and (max_size + i == len(seq) or seq[max_size + i] != "#")
        ):
            left = count_possible(seq[: max(0, i - 1)], sizes[:idx_max_size])
            right = count_possible(seq[i + max_size + 1 :], sizes[idx_max_size + 1 :])
            num_solutions += left * right
    return num_solutions


def day12_part1(data):
    return sum(count_possible(line + ".", sizes) for line, sizes in data)


def day12_part2(data):
    return sum(
        count_possible("?".join([line] * 5) + ".", sizes * 5) for line, sizes in data
    )


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day12_test.txt")


def test_day12_part1(test_data):
    assert day12_part1(test_data) == 21


def test_day12_part2(test_data):
    assert day12_part2(test_data) == 525152


if __name__ == "__main__":
    input_data = parse_input("data/day12.txt")

    print("Day 12 Part 1:")
    print(day12_part1(input_data))

    print("Day 12 Part 2:")
    print(day12_part2(input_data))
