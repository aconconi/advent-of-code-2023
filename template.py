"""
    Advent of Code 2023
    Day 00:
"""

# pylint: skip-file
import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read()


def day00_part1(data):
    pass


def day00_part2(data):
    pass


"""
@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day00_test.txt")


def test_day00_part1(test_data):
    assert day00_part1(test_data)

def test_day00_part2(test_data):
    assert day00_part2(test_data)
"""

if __name__ == "__main__":
    input_data = parse_input("data/day00_test.txt")

    print("Day 00 Part 1:")
    print(day00_part1(input_data))  # Correct answer is

    print("Day 00 Part 2:")
    print(day00_part2(input_data))  # Correct answer is
