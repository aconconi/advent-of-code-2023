"""
    Advent of Code 2023
    Day 02: Cube Conundrum
"""

import re

import pytest


def parse_input(file_name: str) -> list[list[dict[str, int]]]:
    with open(file_name, "r", encoding="ascii") as data_file:
        return [parse_game(line) for line in data_file.read().splitlines()]


def parse_game(line: str) -> list[dict[str, int]]:
    pattern = re.compile(r"(\d* green|\d* blue|\d* red)(?:, |$)")
    matches = re.split("; ", line)
    color_entries = [pattern.findall(match) for match in matches]
    return list(map(parse_revealed_cubes, color_entries))


def parse_revealed_cubes(entry: list[str]) -> dict[str, int]:
    return {
        color: int(quantity) for quantity, color in (item.split() for item in entry)
    }


def day02_part1(data: list[list[dict[str, int]]]) -> int:
    REQUIRED = {"red": 12, "green": 13, "blue": 14}

    def is_possible_game(sets_of_cubes):
        return all(
            revealed_quantity <= REQUIRED[color]
            for cubes in sets_of_cubes
            for color, revealed_quantity in cubes.items()
        )

    return sum(
        game_id
        for game_id, sets_of_cubes in enumerate(data, start=1)
        if is_possible_game(sets_of_cubes)
    )


def day02_part2(data: list[list[dict[str, int]]]) -> int:
    def fewest_required(sets_of_cubes):
        return {
            color: max(cubes.get(color, 0) for cubes in sets_of_cubes)
            for color in ["red", "green", "blue"]
        }

    def power_cubes(cubes):
        return cubes["red"] * cubes["blue"] * cubes["green"]

    return sum(power_cubes(fewest_required(sets_of_cubes)) for sets_of_cubes in data)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day02_test.txt")


def test_day02_part1(test_data):
    assert day02_part1(test_data) == 8


def test_day02_part2(test_data):
    assert day02_part2(test_data) == 2286


if __name__ == "__main__":
    input_data = parse_input("data/day02.txt")

    print("Day 02 Part 1:")
    print(day02_part1(input_data))

    print("Day 02 Part 2:")
    print(day02_part2(input_data))
