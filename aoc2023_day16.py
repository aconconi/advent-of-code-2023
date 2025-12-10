"""
    Advent of Code 2023
    Day 16: The Floor Will Be Lava
"""

from itertools import chain
from collections.abc import Generator

import pytest

Vect2D = tuple[int, int]
Beam = tuple[Vect2D, Vect2D]
Grid = list[str]

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
V_DIRS = [UP, DOWN]
H_DIRS = [LEFT, RIGHT]

MIRROR = {
    "/": {LEFT: [DOWN], RIGHT: [UP], UP: [RIGHT], DOWN: [LEFT]},
    "\\": {LEFT: [UP], RIGHT: [DOWN], UP: [LEFT], DOWN: [RIGHT]},
}


BEHAVIOR = {
    ".": lambda d: [d],
    "-": lambda d: [d] if d in H_DIRS else H_DIRS,
    "|": lambda d: [d] if d in V_DIRS else V_DIRS,
    "/": lambda d: MIRROR["/"][d],
    "\\": lambda d: MIRROR["\\"][d],
}


def is_valid(grid: Grid, location: Vect2D) -> bool:
    heigth, width = len(grid), len(grid[0])
    r, c = location
    return 0 <= r < heigth and 0 <= c < width


def beam_step(grid: Grid, beam: Beam) -> Generator[Beam, None, None]:
    (r, c), (dr, dc) = beam
    new_location = (new_row, new_col) = (r + dr, c + dc)
    if is_valid(grid, new_location):
        _, direction = beam
        symbol = grid[new_row][new_col]
        for new_direction in BEHAVIOR[symbol](direction):
            yield new_location, new_direction


def parse_input(file_name: str) -> Grid:
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().splitlines()


def solve(grid: Grid, start: Beam) -> int:
    beams = [start]
    seen = set()
    while beams:
        beam = beams.pop()
        seen.add(beam)
        beams.extend(
            new_beam for new_beam in beam_step(grid, beam) if new_beam not in seen
        )
    return len(set(location for location, _ in seen)) - 1


def day16_part1(data: Grid) -> int:
    return solve(data, ((0, -1), RIGHT))


def day16_part2(data: Grid) -> int:
    heigth, width = len(data), len(data[0])
    starts = chain(
        (((r, -1), RIGHT) for r in range(heigth)),
        (((r, width), LEFT) for r in range(heigth)),
        (((-1, c), DOWN) for c in range(width)),
        (((heigth, c), RIGHT) for c in range(width)),
    )
    return max(solve(data, start) for start in starts)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day16_test.txt")


def test_day16_part1(test_data):
    assert day16_part1(test_data) == 46


def test_day16_part2(test_data):
    assert day16_part2(test_data) == 51


if __name__ == "__main__":
    input_data = parse_input("data/day16.txt")

    print("Day 16 Part 1:")
    print(day16_part1(input_data))

    print("Day 16 Part 2:")
    print(day16_part2(input_data))
