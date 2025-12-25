import re

from helper import exec_tasks, print_ex, read_file

DEER_MATCHER = re.compile(r"(?P<name>[A-Za-z]+) can fly (?P<fly_speed>[0-9]+) km/s for (?P<fly_time>[0-9]+) seconds, "
                          r"but then must rest for (?P<rest_time>[0-9]+) seconds.")


class Deer:
    name: str
    fly_speed: int
    fly_time: int
    rest_time: int
    cycle_time: int

    def __init__(self, name: str, fly_speed: int, fly_time: int, rest_time: int) -> None:
        self.name = name
        self.fly_speed = fly_speed
        self.fly_time = fly_time
        self.rest_time = rest_time
        self.cycle_time = fly_time + rest_time

    def is_flying(self, moment: int) -> bool:
        return moment % self.cycle_time < self.fly_time


type Data = list[Deer]


def parse_data(lines: list[str]) -> Data:
    return [parse_deer(line) for line in lines]


def parse_deer(line: str) -> Deer:
    matched = DEER_MATCHER.match(line)
    return Deer(
        matched.group("name"),
        int(matched.group("fly_speed")),
        int(matched.group("fly_time")),
        int(matched.group("rest_time"))
    )


def task1(data: Data, race_time: int) -> int:
    return compute_max_deer(data, race_time)


def task2(data: Data, race_time: int) -> int:
    points: list[int] = len(data) * [0]
    positions: list[int] = len(data) * [0]
    for moment in range(race_time):
        for index, deer in enumerate(data):
            if deer.is_flying(moment):
                positions[index] += deer.fly_speed
        max_pos = max(positions)
        for index, position in enumerate(positions):
            if position == max_pos:
                points[index] += 1
    return max(points)


def compute_max_deer(data: Data, race_time: int) -> int:
    return max(compute_deer_pos(deer, race_time) for deer in data)


def compute_deer_pos(deer: Deer, race_time: int) -> int:
    cycle_distance = deer.fly_time * deer.fly_speed
    return (race_time // deer.cycle_time * cycle_distance
            + (min(race_time % deer.cycle_time, deer.fly_time) * deer.fly_speed))


def main():
    exec_tasks(parse_data,
               lambda d: task1(d, 1000),
               lambda d: task2(d, 1000),
               read_file('../data/samples/year15/day15_14.sample'),
               1120,
               689)
    exec_tasks(parse_data,
               lambda d: task1(d, 2503),
               lambda d: task2(d, 2503),
               read_file('../data/input/year15/day15_14.in'),
               2660,
               1256)


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex(ex)
