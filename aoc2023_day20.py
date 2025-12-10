"""
Advent of Code 2023
Day 20:
"""

# pylint: skip-file


def parse_input(file_name):
    with open(file_name, "r", encoding="ascii") as data_file:
        lines = data_file.read().splitlines()
    for line in lines:
        source, _, *destinations = line.replace(",", "").split(" ")
        print(source, destinations)


class Pulse:
    def __init__(self, sender, receiver, level):
        self.sender = sender
        self.receiver = receiver
        self.level = level  # "low" or "high"


class Module:
    def __init__(self, name):
        self.name = name
        self.destinations = []

    def send(self, level, queue):
        for dest in self.destinations:
            queue.append(Pulse(self, dest, level))

    def receive(self, pulse, queue):
        raise NotImplementedError


class FlipFlop(Module):
    def __init__(self, name):
        super().__init__(name)
        self.state = False  # False = off, True = on

    def receive(self, pulse, queue):
        if pulse.level == "high":
            return  # Ignore high pulses
        self.state = not self.state
        self.send("high" if self.state else "low", queue)


class Conjunction(Module):
    def __init__(self, name):
        super().__init__(name)
        self.memory = {}

    def remember_input(self, input_module):
        self.memory[input_module.name] = "low"

    def receive(self, pulse, queue):
        self.memory[pulse.sender.name] = pulse.level
        if all(level == "high" for level in self.memory.values()):
            self.send("low", queue)
        else:
            self.send("high", queue)


class Broadcaster(Module):
    def receive(self, pulse, queue):
        self.send(pulse.level, queue)


class Button:
    def __init__(self, broadcaster):
        self.broadcaster = broadcaster

    def press(self, queue):
        queue.append(Pulse(self, self.broadcaster, "low"))


MODULE_TYPES = {"%": FlipFlop, "&": Conjunction}


def day20_part1(data):
    pass


def day20_part2(data):
    pass


"""
@pytest.fixture(autouse=True, name="test_data")
def fixture_test_data():
    return parse_input("data/day20_test.txt")


def test_day20_part1(test_data):
    assert day20_part1(test_data)

def test_day20_part2(test_data):
    assert day20_part2(test_data)
"""

if __name__ == "__main__":
    input_data = parse_input("data/day20_test.txt")

    print("Day 20 Part 1:")
    print(day20_part1(input_data))

    print("Day 20 Part 2:")
    print(day20_part2(input_data))
