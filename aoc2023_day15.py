"""
    Advent of Code 2023
    Day 15: Lens Library
"""

from dataclasses import dataclass
from functools import reduce

import pytest


@dataclass
class Lens:
    label: str
    focal_length: int


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().split(",")


def hash_str(s: str) -> int:
    def hash_char(current: int, char: str) -> int:
        return (current + ord(char)) * 17 % 256

    return reduce(hash_char, s, 0)


def day15_part1(data):
    return sum(hash_str(s) for s in data)


def day15_part2(data):
    boxes = [[] for _ in range(256)]

    for s in data:
        label, focal_length = (s[:-1], None) if s[-1] == "-" else (s[:-2], int(s[-1]))
        box_idx = hash_str(label)
        lens = next((lens for lens in boxes[box_idx] if lens.label == label), None)
        if not focal_length:
            # this is a "-" operation
            if lens:
                boxes[box_idx].remove(lens)
        else:
            # this is a "=" operation
            if lens:
                lens.focal_length = focal_length
            else:
                boxes[box_idx].append(Lens(label, focal_length))

    # return total focusing power
    return sum(
        sum(
            (box_idx + 1) * slot * lens.focal_length
            for slot, lens in enumerate(box, start=1)
        )
        for box_idx, box in enumerate(boxes)
    )


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day15_test.txt")


def test_day15_part1(test_data):
    assert day15_part1(test_data) == 1320


def test_day15_part2(test_data):
    assert day15_part2(test_data) == 145


if __name__ == "__main__":
    input_data = parse_input("data/day15.txt")

    print("Day 15 Part 1:")
    print(day15_part1(input_data))  # Correct answer is 522547

    print("Day 15 Part 2:")
    print(day15_part2(input_data))  # Correct answer is 229271
