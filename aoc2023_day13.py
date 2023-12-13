"""
    Advent of Code 2023
    Day 13: Point of Incidence
"""


import pytest

Rows = list[str]

def parse_input(file_name: str) -> list[Rows]:
    with open(file_name, "r", encoding="ascii") as data_file:
        return [pattern.splitlines() for pattern in data_file.read().split("\n\n")]


def transpose(pattern: Rows) -> Rows:
    return list(map("".join, zip(*pattern)))


def count_differences(rows_a: Rows, rows_b: Rows, max_count: int=0) -> int:
    num_differences = 0
    for row_a, row_b in zip(rows_a, rows_b):
        num_differences += sum(char_a != char_b for char_a, char_b in zip(row_a, row_b))
        if num_differences > max_count:
            break
    return num_differences


def count_reflections(pattern: Rows, allowed_smudges: int=0) -> int:
    height = len(pattern)
    for line_idx in range(1, height // 2 + 1):
        # stopping at mid height is enough for detecting simmetries

        rows_a = pattern[:line_idx]
        rows_b = pattern[line_idx : 2 * line_idx][::-1]
        num_differences = count_differences(rows_a, rows_b, allowed_smudges)
        if num_differences == allowed_smudges:
            return line_idx

        rows_a = pattern[height - 2 * line_idx : height - line_idx]
        rows_b = pattern[height - line_idx :][::-1]
        num_differences = count_differences(rows_a, rows_b, allowed_smudges)
        if num_differences == allowed_smudges:
            return height - line_idx

    return 0


def day13_part1(data: list[Rows]) -> int:
    return sum(
        100 * count_reflections(pattern) + count_reflections(transpose(pattern))
        for pattern in data
    )


def day13_part2(data: list[Rows]) -> int:
    return sum(
        100 * count_reflections(pattern, allowed_smudges=1)
        + count_reflections(transpose(pattern), allowed_smudges=1)
        for pattern in data
    )


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day13_test.txt")


def test_day13_part1(test_data):
    assert day13_part1(test_data) == 405


def test_day13_part2(test_data):
    assert day13_part2(test_data) == 400


if __name__ == "__main__":
    input_data = parse_input("data/day13.txt")

    print("Day 13 Part 1:")
    print(day13_part1(input_data))  # Correct answer is 30802

    print("Day 13 Part 2:")
    print(day13_part2(input_data))  # Correct answer is 37876
