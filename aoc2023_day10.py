"""
    Advent of Code 2023
    Day 10: Pipe Maze
"""

from collections import deque

import pytest

Node = tuple[int, int]
Path = list[Node]
Graph = dict[Node, list[Node]]


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        return generate_graph(data_file.read().splitlines())


SYMBOL_TO_DIR = {
    "|": ["N", "S"],
    "-": ["W", "E"],
    "L": ["N", "E"],
    "J": ["N", "W"],
    "7": ["S", "W"],
    "F": ["S", "E"],
    ".": [],
    "S": [],
}

DIR_TO_DELTA = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}


def generate_graph(grid: list[str]) -> tuple[Graph, Node | None]:
    graph = {}
    start = None
    n_rows, n_cols = len(grid), len(grid[0])

    def gen_edges(r, c, symbol):
        for direction in SYMBOL_TO_DIR[symbol]:
            dr, dc = DIR_TO_DELTA[direction]
            neigh_r, neigh_c = r + dr, c + dc
            if 0 <= r < n_rows and 0 <= c < n_cols:
                yield neigh_r, neigh_c

    for i, row in enumerate(grid):
        for j, symbol in enumerate(row):
            if symbol == "S":
                start = (i, j)
            else:
                graph[(i, j)] = list(gen_edges(i, j, symbol))

    graph[start] = [node for node, neighbors in graph.items() if start in neighbors]
    return graph, start


def find_loop(graph: Graph, start: Node) -> Path:
    stack = [[start]]
    while stack:
        path = stack.pop()
        node = path[-1]
        for neigh in graph[node]:
            if neigh == start and len(path) > 2:
                # loop found
                return path + [neigh]
            if neigh not in path:
                stack.append(path + [neigh])
    return []


def is_point_inside_loop(
    loop: Path, point: Node, include_perimeter: bool = False
) -> bool:
    # Winding number algorithm
    # https://en.wikipedia.org/wiki/Winding_number

    if point in loop and not include_perimeter:
        return False

    x, y = point
    winding_number = 0
    for i, (x1, y1) in enumerate(loop):
        x2, y2 = loop[(i + 1) % len(loop)]
        if y1 <= y < y2 or y2 <= y < y1:
            cross_product = (x2 - x1) * (y - y1) - (x - x1) * (y2 - y1)
            if cross_product > 0:
                winding_number += 1
            elif cross_product < 0:
                winding_number -= 1

    return winding_number != 0


def flood_fill(graph: Graph, loop: Path) -> set[Node]:
    # Flood fill algorithm
    # https://en.wikipedia.org/wiki/Flood_fill

    def gen_adjacent(node):
        r, c = node
        for dr, dc in DIR_TO_DELTA.values():
            neigh_r, neigh_c = r + dr, c + dc
            if (neigh_r, neigh_c) in graph:
                yield neigh_r, neigh_c

    visited = set(loop)
    area = set()

    adjacent_to_loop = set(neigh for node in loop for neigh in gen_adjacent(node))

    queue = deque(
        [node for node in adjacent_to_loop if is_point_inside_loop(loop, node)]
    )

    while queue:
        current_node = queue.popleft()
        if current_node not in visited:
            visited.add(current_node)
            area.add(current_node)
            queue.extend(
                neighbor
                for neighbor in gen_adjacent(current_node)
                if neighbor not in visited
            )
    return area


def day10_part1(data):
    graph, start = data
    loop = find_loop(graph, start)
    return len(loop) // 2 if loop else None


def day10_part2(data):
    graph, start = data
    loop = find_loop(graph, start)
    area = flood_fill(graph, loop)
    return len(area)


@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return [parse_input(f"data/day10_test{num}.txt") for num in ["1", "2", "3", "4"]]


def test_day10_part1(test_data):
    assert day10_part1(test_data[0]) == 4


def test_day10_part2(test_data):
    assert day10_part2(test_data[1]) == 4
    assert day10_part2(test_data[2]) == 8
    assert day10_part2(test_data[3]) == 10


if __name__ == "__main__":
    input_data = parse_input("data/day10.txt")

    print("Day 10 Part 1:")
    print(day10_part1(input_data))  # Correct answer is 6931

    print("Day 10 Part 2:")
    print(day10_part2(input_data))  # Correct answer is
