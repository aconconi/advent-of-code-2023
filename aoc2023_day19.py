"""
    Advent of Code 2023
    Day 19: Aplenty
"""


import pytest
import re

from dataclasses import dataclass
from operator import lt, gt
import re
from math import prod


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_string(cls, string: str) -> "Part":
        pattern = re.compile(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}")
        match = pattern.match(string)
        if not match:
            raise ValueError("Invalid string format for Part")
        
        x, m, a, s = map(int, match.groups())
        return cls(x, m, a, s)

    def apply_workflow(self, workflows, name):
        if name in {"A", "R"}:
            return name == "A"

        conditions, default = workflows[name]
        for condition in conditions:
            field, op, comp_value, result = re.match(
                r"(\w+)([<>]=?)(\d+):(\w+)", condition
            ).groups()
            comp_func = lt if op == "<" else gt
            if comp_func(getattr(self, field), int(comp_value)):
                return self.apply_workflow(workflows, result)
        return self.apply_workflow(workflows, default)

    def total_rating(self):
        return self.x + self.m + self.a + self.s


def decode_workflow(line):
    matched = re.match(r"(\w+){(.*)}", line)
    if not matched:
        return None
    name, conditions = matched.groups()
    conditions = conditions.split(",")
    return name, (conditions[:-1], conditions[-1])


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        workflows, ratings = data_file.read().split("\n\n")
        return workflows.splitlines(), ratings.splitlines()


def day19_part1(data):
    wf_data, parts_data = data
    workflows = dict(decode_workflow(line) for line in wf_data)
    parts = [Part.from_string(line) for line in parts_data]
    return sum(
        part.total_rating() for part in parts if part.apply_workflow(workflows, "in")
    )


class PartWithRange:
    def __init__(self):
        self.intervals = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}

    def split_interval(self, condition):
        field, op, comp_value, result = re.match(
            r"(\w+)([<>]=?)(\d+):(\w+)", condition
        ).groups()
        

        low, high = self.intervals[field] 
        cond_low =  (lt if op == "<" else gt)(low, int(comp_value))
        cond_high =  (lt if op == "<" else gt)(high, int(comp_value))

        if cond_low and cond_high:
            matching_interval = (low, high)
            non_matching_interval = None
        elif not cond_low and not cond_high:
            matching_interval = None
            non_matching_interval = (low, high)
        else:
            if cond_low:
                matching_interval = (low, high - 1)
                non_matching_interval = (high, high)
            else:
                matching_interval = (low + 1, high)
                non_matching_interval = (low, low)
        return matching_interval, non_matching_interval


    def total_combinations(self):
        return prod(high - low for low, high in self.intervals.values())
    

def day19_part2(data):
    start = ({"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}, "in")

    todo = [start]




@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day19_test.txt")


def test_day19_part1(test_data):
    assert day19_part1(test_data) == 19114


"""
def test_day19_part2(test_data):
    assert day19_part2(test_data)
"""

if __name__ == "__main__":
    input_data = parse_input("data/day19.txt")

    print("Day 19 Part 1:")
    print(day19_part1(input_data))  # Correct answer is 353046

    print("Day 19 Part 2:")
    print(day19_part2(input_data))  # Correct answer is
