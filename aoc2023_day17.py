"""
    Advent of Code 2023
    Day 17: Clumsy Crucible
"""

import heapq

import pytest

Vect2D = tuple[int, int]
Graph = dict[Vect2D, int]
Node = tuple[Vect2D, Vect2D, int]

UP: Vect2D = (-1, 0)
DOWN: Vect2D = (1, 0)
LEFT: Vect2D = (0, -1)
RIGHT: Vect2D = (0, 1)
DIRECTIONS: list[Vect2D] = [UP, DOWN, LEFT, RIGHT]
OPPOSITE: dict[Vect2D, Vect2D] = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


def parse_input(file_name: str) -> tuple[Graph, Vect2D]:
    with open(file_name, "r", encoding="ascii") as data_file:
        grid = data_file.read().splitlines()
    graph = {
        (i, j): int(heat_loss)
        for i, row in enumerate(grid)
        for j, heat_loss in enumerate(row)
    }
    destination = (len(grid) - 1, len(grid[0]) - 1)
    return graph, destination


def get_neighbours(graph: Graph, node: Node, min_moves: int, max_moves: int):
    position, direction, moves = node

    for new_direction in DIRECTIONS:
        # Cannot reverse movement.
        if new_direction == OPPOSITE[direction]:
            continue

        # Must stay within the grid.
        (r, c), (dr, dc) = position, direction
        new_position = r + dr, c + dc
        if new_position not in graph:
            continue

        # Increment moves counter if proceeding in the same direction,
        # else reset it to the initial value 1.
        new_moves = (moves + 1) if direction == new_direction else 1

        # Cannot proceed in the same direction for more than max_moves.
        if new_moves > max_moves:
            continue

        # Cannot change direction before completing at least min_moves.
        if direction != new_direction and moves < min_moves:
            continue

        # If we get here, this is a valid neighbour!
        yield (new_position, new_direction, new_moves)


def solve(graph: Graph, destination: Vect2D, min_moves: int, max_moves: int) -> int:
    # Thanks Prof. Dijkstra
    start = (0, 0)
    distances = {}
    todo = []

    # Initialize heap with the start location and the two possible directions.
    # Note the number of initial moves is set to 1 and no cost is incurred.
    for initial_direction in [RIGHT, DOWN]:
        heapq.heappush(todo, (0, (start, initial_direction, 1)))

    while todo:
        (cost, current) = heapq.heappop(todo)
        if current in distances:
            # We've already seen a node with the same position, direction, and moves.
            continue
        distances[current] = cost
        for neigh in get_neighbours(graph, current, min_moves, max_moves):
            position, _, _ = neigh
            new_cost = cost + graph[position]
            if neigh not in distances or new_cost < distances[current]:
                # Neigh was never seen, or its new cost is better.
                heapq.heappush(todo, (new_cost, neigh))

    return min(
        cost
        for (position, _, moves), cost in distances.items()
        if position == destination and moves >= min_moves
    )


def day17_part1(data: tuple[Graph, Vect2D]) -> int:
    graph, destination = data
    return solve(graph, destination, 1, 3)


def day17_part2(data: tuple[Graph, Vect2D]) -> int:
    graph, destination = data
    return solve(graph, destination, 4, 10)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day17_test.txt")


def test_day17_part1(test_data):
    assert day17_part1(test_data) == 102


def test_day17_part2(test_data):
    assert day17_part2(test_data) == 94


if __name__ == "__main__":
    input_data = parse_input("data/day17.txt")

    print("Day 17 Part 1:")
    print(day17_part1(input_data))  # Correct answer is 758

    print("Day 17 Part 2:")
    print(day17_part2(input_data))  # Correct answer is 892
