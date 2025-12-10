"""
    Advent of Code 2023
    Day 04: Scratchcards
"""

import re

import pytest


def parse_input(file_name):
    pattern = re.compile(r"Card ([\d ]+): ([\d ]+) \| ([\d ]+)")

    def parse_line(line):
        if match := pattern.match(line):
            return (
                int(match.group(1)),
                set(map(int, match.group(2).split())),
                set(map(int, match.group(3).split())),
            )
        raise ValueError(f"Error parsing line {line}")

    with open(file_name, "r", encoding="ascii") as data_file:
        return [parse_line(line) for line in data_file.read().splitlines()]


def day04_part1(cards):
    def card_score(num_matches):
        return 0 if num_matches == 0 else 2 ** (num_matches - 1)

    return sum(card_score(len(winning & have)) for _, winning, have in cards)


def day04_part2_recursion(cards):
    """Just wanted to leave also a first version of the solution using recursion."""
    matches = {card_id: len(winning & have) for card_id, winning, have in cards}
    quantity = {card_id: 0 for card_id, _, _ in cards}
    max_card_id = len(cards)

    def update_quantity(card_id):
        quantity[card_id] += 1
        for below in range(card_id + 1, card_id + matches[card_id] + 1):
            if below <= max_card_id:
                update_quantity(below)

    for card_id, _, _ in cards:
        update_quantity(card_id)

    return sum(quantity.values())


def day04_part2(cards):
    matches = {card_id: len(winning & have) for card_id, winning, have in cards}
    quantity = {card_id: 0 for card_id, _, _ in cards}
    max_card_id = len(cards)
    stack = [card_id for card_id, _, _ in cards]
    while stack:
        current_card_id = stack.pop()
        quantity[current_card_id] += 1
        stack.extend(
            below
            for below in range(
                current_card_id + 1,
                current_card_id + matches[current_card_id] + 1
            )
            if below <= max_card_id
        )
    return sum(quantity.values())


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day04_test.txt")


def test_day04_part1(test_data):
    assert day04_part1(test_data) == 13


def test_day04_part2(test_data):
    assert day04_part2(test_data) == 30


if __name__ == "__main__":
    input_data = parse_input("data/day04.txt")

    print("Day 04 Part 1:")
    print(day04_part1(input_data))

    print("Day 04 Part 2:")
    print(day04_part2(input_data))
