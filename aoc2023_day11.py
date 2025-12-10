"""
    Advent of Code 2023
    Day 11: Cosmic Expansion
"""

from itertools import combinations

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        grid = data_file.read().splitlines()
        num_rows, num_cols = len(grid), len(grid[0])
        galaxies = {
            (i, j)
            for i, row in enumerate(grid)
            for j, symbol in enumerate(row)
            if symbol == "#"
        }
    empty_rows = set(range(num_rows)) - set(i for i, _ in galaxies)
    empty_cols = set(range(num_cols)) - set(j for _, j in galaxies)
    return galaxies, empty_rows, empty_cols


def distance(
    a: tuple[int, int],
    b: tuple[int, int],
    empty_rows: set[int],
    empty_cols: set[int],
    scale: int,
) -> int:
    a_row, a_col = a
    b_row, b_col = b
    num_scaled_rows = sum(a_row < r < b_row or b_row < r < a_row for r in empty_rows)
    num_scaled_cols = sum(a_col < c < b_col or b_col < c < a_col for c in empty_cols)
    base_dist = abs(b_row - a_row) + abs(b_col - a_col)
    return base_dist + (num_scaled_rows + num_scaled_cols) * (scale - 1)


def day11_part1(data):
    galaxies, empty_rows, empty_cols = data
    return sum(
        distance(a, b, empty_rows, empty_cols, 2) for a, b in combinations(galaxies, 2)
    )


def day11_part2(data):
    galaxies, empty_rows, empty_cols = data
    return sum(
        distance(a, b, empty_rows, empty_cols, 1_000_000)
        for a, b in combinations(galaxies, 2)
    )


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day11_test.txt")


def test_day11_part1(test_data):
    assert day11_part1(test_data) == 374


def test_day11_part2(test_data):
    assert day11_part2(test_data) == 82000210


if __name__ == "__main__":
    input_data = parse_input("data/day11.txt")

    print("Day 11 Part 1:")
    print(day11_part1(input_data))

    print("Day 11 Part 2:")
    print(day11_part2(input_data))
