"""
    Advent of Code 2023
    Day 03: Gear Ratios
"""

from itertools import product

import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        grid = data_file.read().splitlines()

    numbers = []
    symbols = set()
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == ".":
                continue
            if char.isdigit():
                if numbers and (i, j - 1) in numbers[-1]:
                    numbers[-1].append((i, j))
                else:
                    numbers.append([(i, j)])
            else:
                symbols.add((i, j))

    return grid, [tuple(number) for number in numbers], symbols


def get_neighbors(pos):
    i, j = pos
    return (
        (i + di, j + dj)
        for di, dj in product([-1, 0, 1], repeat=2)
        if (di, dj) != (0, 0)
    )


def get_outer_edge(positions):
    min_col = min(pos[1] for pos in positions)
    max_col = max(pos[1] for pos in positions)
    min_row = min(pos[0] for pos in positions)
    max_row = max(pos[0] for pos in positions)
    for col in range(min_col - 1, max_col + 2):
        yield min_row - 1, col
    for row in range(min_row, max_row + 1):
        yield row, min_col - 1
        yield row, max_col + 1
    for col in range(min_col - 1, max_col + 2):
        yield max_row + 1, col


def number_from_digit_coordinates(grid, digit_coordinates):
    return int("".join(grid[i][j] for (i, j) in digit_coordinates))


def day03_part1(data):
    grid, numbers, symbols = data
    return sum(
        number_from_digit_coordinates(grid, number)
        for number in numbers
        if symbols & set(get_outer_edge(number))
    )


def day03_part2(data):
    grid, numbers, symbols = data
    ans = 0
    for symbol in symbols:
        i, j = symbol
        if grid[i][j] != "*":
            continue
        symbol_neighbors = set(get_neighbors(symbol))
        adjacent_numbers = [
            number_from_digit_coordinates(grid, number)
            for number in numbers
            if set(number) & symbol_neighbors
        ]
        if len(adjacent_numbers) > 1:
            # this is a gear ratio
            ans += adjacent_numbers[0] * adjacent_numbers[1]
    return ans


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day03_test.txt")


def test_day03_part1(test_data):
    assert day03_part1(test_data) == 4361


def test_day03_part2(test_data):
    assert day03_part2(test_data) == 467835


if __name__ == "__main__":
    input_data = parse_input("data/day03.txt")

    print("Day 03 Part 1:")
    print(day03_part1(input_data))  # Correct answer is 536202

    print("Day 03 Part 2:")
    print(day03_part2(input_data))  # Correct answer is 78272573
