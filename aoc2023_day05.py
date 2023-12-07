"""
    Advent of Code 2023
    Day 05:
"""

from functools import reduce

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        first, *others = data_file.read().split("\n\n")
    seeds = list(map(int, first.split(":")[1].split()))
    sections = [
        [tuple(map(int, line.split())) for line in chunk.split("\n")[1:]]
        for chunk in others
    ]
    return seeds, sections


def convert_single(x: int, rules: list[tuple[int, int, int]]) -> int:
    return next(
        (
            x - source_start + dest_start
            for dest_start, source_start, size in rules
            if source_start <= x < source_start + size
        ),
        x,
    )


def grouper(n, iterable):
    args = [iter(iterable)] * n
    return zip(*args)


def convert_range(
    ranges: list[tuple[int, int]], rules: list[tuple[int, int, int]]
) -> list[tuple[int, int]]:
    locations = []

    for dest_start, source_start, size in rules:
        source_end = source_start + size
        new_ranges = []

        for a, b in ranges:
            before = (a, min(b, source_start))
            inter = (max(a, source_start), min(source_end, b))
            after = (max(source_end, a), b)

            new_ranges.extend(
                interval for interval in [before, after] if interval[1] > interval[0]
            )

            locations.extend(
                (
                    inter[0] - source_start + dest_start,
                    inter[1] - source_start + dest_start,
                )
                for inter in [inter]
                if inter[1] > inter[0]
            )
        ranges = new_ranges

    return locations + ranges


def day05_part1(data):
    seeds, sections = data

    def location(seed):
        return reduce(convert_single, sections, seed)

    return min(location(seed) for seed in seeds)


def day05_part2(data):
    seeds, sections = data

    def min_location_seed_range(seed_range: tuple[int, int]) -> int:
        start_seed, size = seed_range
        return min(reduce(convert_range, sections, [(start_seed, start_seed + size)]))[
            0
        ]

    return min(min_location_seed_range(seed_range) for seed_range in grouper(2, seeds))


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day05_test.txt")


def test_day05_part1(test_data):
    assert day05_part1(test_data) == 35


def test_day05_part2(test_data):
    assert day05_part2(test_data) == 46


if __name__ == "__main__":
    input_data = parse_input("data/day05.txt")

    print("Day 05 Part 1:")
    print(day05_part1(input_data))  # Correct answer is 51580674

    print("Day 05 Part 2:")
    print(day05_part2(input_data))  # Correct answer is 99751240
