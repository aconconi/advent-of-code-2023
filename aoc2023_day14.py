"""
    Advent of Code 2023
    Day 14: Parabolic Reflector Dish
"""

import numpy as np
import pytest


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().splitlines()


def tilt_north(grid):
    heigth = len(grid)
    for i, row in enumerate(grid):
        for j, symbol in enumerate(row):
            if symbol == ".":
                # look for first rounded rock that could roll into this space
                k = next((k for k in range(i + 1, heigth) if grid[k][j] != "."), None)
                if k and grid[k][j] == "O":
                    grid[i][j] = "O"
                    grid[k][j] = "."


def total_load_north_beam(grid):
    return sum(i * row.count("O") for i, row in enumerate(reversed(grid), start=1))


def tilt_cycle(grid):
    # A cycle tilts the grid in North, West, South, East direction.
    # Because we only want to use the tilt_north function,
    # we rotate the grid, then tilt north, then rotate back.
    # N, W, S, E correspond to 0, -1, 2, 1 parameters for np.rot90.
    for rotation in (0, -1, 2, 1):
        grid = np.rot90(grid, rotation)
        tilt_north(grid)
        grid = np.rot90(grid, -rotation)
    return grid


def concatenate_grid(grid):
    return "".join("".join(row) for row in grid)


def apply_periodic_function(periodic_func, initial, hash_func, num_cycles):
    seen = {}
    current = initial

    for cycle in range(num_cycles):
        hashed = hash_func(current)
        if hashed not in seen:
            seen[hashed] = cycle
            current = periodic_func(current)
        else:
            # Detected a period
            cycle_difference = cycle - seen[hashed]
            remaining_cycles = (num_cycles - cycle) % cycle_difference
            # Fast forward
            for _ in range(remaining_cycles):
                current = periodic_func(current)
            break

    return current


def day14_part1(data):
    grid = [list(line) for line in data]
    tilt_north(grid)
    return total_load_north_beam(grid)


def day14_part2(data):
    grid = np.array([list(line) for line in data])
    apply_periodic_function(
        periodic_func=tilt_cycle,
        initial=grid,
        hash_func=concatenate_grid,
        num_cycles=1_000_000_000,
    )
    return total_load_north_beam(grid.tolist())


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day14_test.txt")


def test_day14_part1(test_data):
    assert day14_part1(test_data) == 136


def test_day14_part2(test_data):
    assert day14_part2(test_data) == 64


if __name__ == "__main__":
    input_data = parse_input("data/day14.txt")

    print("Day 14 Part 1:")
    print(day14_part1(input_data))

    print("Day 14 Part 2:")
    print(day14_part2(input_data))
