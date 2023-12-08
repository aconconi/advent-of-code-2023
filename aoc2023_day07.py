"""
    Advent of Code 2023
    Day 07: Camel Cards
"""

from collections import Counter

import pytest

CARDS_COUNT_RANK = [
    ([5], 7),              # five of a kind
    ([1, 4], 6),           # four of a kind
    ([2, 3], 5),           # full house
    ([1, 1, 3], 4),        # three of a kind
    ([1, 2, 2], 3),        # two pair
    ([1, 1, 1, 2], 2),     # one pair
    ([1, 1, 1, 1, 1], 1)   # high card
]


def parse_input(file_name):
    def parse_line(line):
        card, bid = line.split()
        return (card, int(bid))

    with open(file_name, "r", encoding="ascii") as data_file:
        return [parse_line(line) for line in data_file.read().splitlines()]


def hand_rank(hand: str, jokers=False) -> tuple[int, tuple[int, ...]]:
    c = Counter(hand)
    if jokers and 0 < (num_jokers := c["J"]) < 5:
        del c["J"]
        most_common_non_joker, _ = c.most_common(1)[0]
        c[most_common_non_joker] += num_jokers
    cards_count = sorted(c.values())

    hand_type = next(
        t for pattern, t in CARDS_COUNT_RANK if cards_count == pattern
    )

    card_ranks = tuple(
        ("J23456789TQKA" if jokers else "23456789TJQKA").index(card) for card in hand
    )

    return (hand_type, card_ranks)


def day07_part1(data):
    sorted_hands = sorted(data, key=lambda x: (hand_rank(x[0])))
    return sum(i * bid for i, (hand, bid) in enumerate(sorted_hands, start=1))


def day07_part2(data):
    sorted_hands = sorted(data, key=lambda x: (hand_rank(x[0], jokers=True)))
    return sum(i * bid for i, (hand, bid) in enumerate(sorted_hands, start=1))


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day07_test.txt")


def test_day07_part1(test_data):
    assert day07_part1(test_data) == 6440


def test_day07_part2(test_data):
    assert day07_part2(test_data) == 5905


if __name__ == "__main__":
    input_data = parse_input("data/day07.txt")

    print("Day 07 Part 1:")
    print(day07_part1(input_data))  # Correct answer is 248453531

    print("Day 07 Part 2:")
    print(day07_part2(input_data))  # Correct answer is 248781813
