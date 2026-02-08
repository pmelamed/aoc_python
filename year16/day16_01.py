from geom2d import Coord2D
from helper import exec_tasks, print_ex, read_file


def parse_data(lines: list[str]) -> list[tuple[str, int]]:
    return [(cmd[:1], int(cmd[1:])) for cmd in lines[0].split(', ')]


def task1(data: list[tuple[str, int]]) -> int:
    pos = Coord2D(0, 0)
    direct = Coord2D(0, 1)
    for cmd in data:
        match cmd[0]:
            case 'R':
                direct = direct.turn_right()
            case 'L':
                direct = direct.turn_left()
        pos += direct * cmd[1]
    return pos.manhattan()


def task2(data: list[tuple[str, int]]) -> int:
    pos = Coord2D(0, 0)
    direct = Coord2D(0, 1)
    visited: set[Coord2D] = {Coord2D(0, 0)}
    for cmd in data:
        match cmd[0]:
            case 'R':
                direct = direct.turn_right()
            case 'L':
                direct = direct.turn_left()
        for step in range( cmd[1] ):
            pos += direct
            if pos in visited:
                return pos.manhattan()
            visited.add(pos)
    return -1


def main():
    exec_tasks(parse_data, task1, task2, read_file('../data/input/year16/day16_01.in'), 271, 153)


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex(ex)
