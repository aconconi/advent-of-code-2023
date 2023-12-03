"""
    Advent of Code 2023
    Day 01: Trebuchet?!
"""

import re
import pytest

LETTERS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
DIGITS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
LETTERS_TO_DIGITS = dict(zip(LETTERS, DIGITS))
RE_LEFT = re.compile(r"\d|" + "|".join(LETTERS))
RE_RIGHT = re.compile(r"\d|" + "|".join(s[::-1] for s in LETTERS))


def parse_input(file_name: str) -> list[str]:
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().splitlines()


def day01_part1(data: list[str]) -> int:
    def get_first_digit(line: str, reverse: bool = False) -> str:
        return next(
            (c for c in (reversed(line) if reverse else line) if c.isdigit()), "0"
        )

    return sum(
        int(get_first_digit(line) + get_first_digit(line, reverse=True))
        for line in data
    )


def day01_part2(data: list[str]) -> int:
    def get_first_digit(line: str, reverse: bool = False) -> str:
        pattern = RE_RIGHT if reverse else RE_LEFT
        if match_obj := pattern.search(line[::-1] if reverse else line):
            m = match_obj[0]
            return m if m.isdigit() else LETTERS_TO_DIGITS[m[::-1] if reverse else m]
        return "0"

    return sum(
        int(get_first_digit(line) + get_first_digit(line, reverse=True))
        for line in data
    )


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return [parse_input("data/day01_test1.txt"), parse_input("data/day01_test2.txt")]


def test_day01_part1(test_data):
    assert day01_part1(test_data[0]) == 142


def test_day01_part2(test_data):
    assert day01_part2(test_data[1]) == 281


if __name__ == "__main__":
    input_data = parse_input("data/day01.txt")

    print("Day 01 Part 1:")
    print(day01_part1(input_data))  # Correct answer is 55488

    print("Day 01 Part 2:")
    print(day01_part2(input_data))  # Correct answer is 55614
