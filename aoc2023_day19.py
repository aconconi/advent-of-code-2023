"""
    Advent of Code 2023
    Day 19: Aplenty
"""


import re
from math import prod

import pytest


class Part:
    """Class representing a Part with x, m, a, s attributes."""

    pattern = re.compile(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}")

    def __init__(self, x, m, a, s):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    @classmethod
    def from_string(cls, string: str) -> "Part":
        match = cls.pattern.match(string)
        if not match:
            raise ValueError("Invalid string format for Part")
        x, m, a, s = map(int, match.groups())
        return cls(x, m, a, s)

    def __getitem__(self, field):
        return getattr(self, field)

    def total_rating(self):
        return sum(getattr(self, attr) for attr in ("x", "m", "a", "s"))

    def __repr__(self):
        return f"(x:{self.x}, m:{self.m}, a:{self.a}, s:{self.s})"

    def apply_workflow(self, workflows, initial_state):
        current_workflow = workflows[initial_state]

        while current_workflow:
            for rule in current_workflow:
                match outcome := rule.evaluate_part(self):
                    case "A":
                        return True
                    case "R":
                        return False
                    case None:
                        continue
                    case _:
                        current_workflow = workflows[outcome]
                        break


class Rule:
    pattern = re.compile(r"([a-z]+)(.)(\d+):(.+)")

    def __init__(self, condition, target):
        self.condition, self.target = condition, target

    @classmethod
    def from_string(cls, rule_s: str):
        match_object = cls.pattern.search(rule_s)
        if match_object:
            key, op, val, target = match_object.groups()
            condition = (key, op, int(val))
        else:
            condition, target = None, rule_s
        return cls(condition, target)

    def inverted_condition(self):
        key, op, val = self.condition
        new_op, new_val = (">", val - 1) if op == "<" else ("<", val + 1)
        return (key, new_op, new_val)

    def evaluate_part(self, part):
        if self.condition is None:
            return self.target
        key, op, val = self.condition
        return (
            self.target
            if (op == "<" and part[key] < val) or (op == ">" and part[key] > val)
            else None
        )

    def __repr__(self):
        return f"({self.condition}, {self.target})"


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        wf_data, parts_data = data_file.read().split("\n\n")
    workflows = {
        name: [Rule.from_string(rule_s) for rule_s in rules_s.split(",")]
        for name, rules_s in (
            line.rstrip("}").split("{") for line in wf_data.splitlines()
        )
    }
    parts = [Part.from_string(line) for line in parts_data.splitlines()]
    return workflows, parts


def add_constraint(constraints, condition):
    # credit: https://github.com/davearussell/advent2023
    key, op, val = condition
    low, high = constraints.get(key, (1, 4000))
    if op == ">":
        if val >= high:
            return None
        low = val + 1
    else:
        if val <= low:
            return None
        high = val - 1
    return dict(constraints, **{key: (low, high)})


def trace_paths(workflows, state):
    name, constraints = state
    for rule in workflows[name]:
        if rule.condition is None:
            cons_true = constraints
        else:
            cons_true = add_constraint(constraints, rule.condition)
            constraints = add_constraint(constraints, rule.inverted_condition())

        if cons_true is not None:
            if rule.target == "A":
                yield cons_true
            elif rule.target != "R":
                yield from trace_paths(workflows, (rule.target, cons_true))


def day19_part1(data):
    workflows, parts = data
    return sum(p.total_rating() for p in parts if p.apply_workflow(workflows, "in"))


def day19_part2(data):
    workflows, _ = data
    initial_state = ("in", {field: (1, 4000) for field in "xmas"})
    paths = trace_paths(workflows, initial_state)
    return sum(prod(hi - lo + 1 for lo, hi in path.values()) for path in paths)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day19_test.txt")


def test_day19_part1(test_data):
    assert day19_part1(test_data) == 19114


def test_day19_part2(test_data):
    assert day19_part2(test_data) == 167409079868000


if __name__ == "__main__":
    input_data = parse_input("data/day19.txt")

    print("Day 19 Part 1:")
    print(day19_part1(input_data))

    print("Day 19 Part 2:")
    print(day19_part2(input_data))
