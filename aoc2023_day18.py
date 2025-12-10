"""
    Advent of Code 2023
    Day 18: Lavaduct Lagoon
"""

from itertools import pairwise

import pytest


def parse_input(file_name: str) -> list[str]:
    with open(file_name, "r", encoding="ascii") as data_file:
        return data_file.read().strip().splitlines()


MOVES = {"U": (0, -1), "D": (0, +1), "L": (-1, 0), "R": (+1, 0)}


def move(position: tuple[int, int], direction: str, steps: int) -> tuple[int, int]:
    x, y = position
    dx, dy = MOVES[direction]
    return x + dx * steps, y + dy * steps


def solve(moves: list[tuple[str, int]]) -> int:
    # The Shoelace Formula is used to calculate the area of a polygon given
    # the coordinates of its vertices. Pick's Theorem provides a way to
    # calculate the area of a lattice polygon (a polygon whose vertices
    # have integer coordinates) based on the number of interior lattice points
    # and the number of lattice points on the boundary.

    current = (0, 0)
    vertices: list[tuple[int, int]] = [current]
    for direction, steps in moves:
        current = move(current, direction, steps)
        vertices.append(current)
    return (
        sum(
            xa * yb - ya * xb + abs(xb - xa + yb - ya)
            for (xa, ya), (xb, yb) in pairwise(vertices)
        )
        // 2
        + 1
    )


def day18_part1(data: list[str]) -> int:
    def decode_instruction(line):
        direction, moves, _ = line.split()
        return direction, int(moves)

    return solve([decode_instruction(line) for line in data])


def day18_part2(data: list[str]) -> int:
    def decode_instruction(line):
        _, _, color = line.split()
        direction = "RDLU"[int(color[7])]
        steps = int(color[2:7], 16)
        return direction, steps

    return solve([decode_instruction(line) for line in data])


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day18_test.txt")


def test_day18_part1(test_data):
    assert day18_part1(test_data) == 62


def test_day18_part2(test_data):
    assert day18_part2(test_data) == 952408144115


if __name__ == "__main__":
    input_data = parse_input("data/day18.txt")

    print("Day 18 Part 1:")
    print(day18_part1(input_data))

    print("Day 18 Part 2:")
    print(day18_part2(input_data))
