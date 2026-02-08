from sympy.strategies.core import switch

from geom2d import Coord2D, Rect2D
from helper import exec_tasks, first_line, print_ex, read_file, turn_cw90, turn_ccw90

DIRECTIONS = {
    'U': Coord2D(0, -1),
    'D': Coord2D(0, 1),
    'L': Coord2D(-1, 0),
    'R': Coord2D(1, 0)
}

PAD_RECT = Rect2D.from_coords(0, 0, 3, 3)
PAD2_RECT = Rect2D.from_coords(0, 0, 5, 5)
PAD2 = [
    "  1  ",
    " 214 ",
    "56789",
    " ABC ",
    "  D  "
]


def parse_data(lines: list[str]) -> list[list[Coord2D]]:
    return [[DIRECTIONS[cmd] for cmd in line] for line in lines]


def task1(data: list[list[Coord2D]]) -> str:
    code = ''
    pos = Coord2D(1, 1)
    for line in data:
        for cmd in line:
            npos = pos + cmd
            if npos in PAD_RECT:
                pos = npos
        code += str(3 * pos.y + pos.x + 1)
    return code


def task2(data: list[list[Coord2D]]) -> str:
    code = ''
    pos = Coord2D(0, 2)
    for line in data:
        for cmd in line:
            npos = pos + cmd
            if npos in PAD2_RECT and PAD2[npos.y][npos.x] != ' ':
                pos = npos
        code += PAD2[pos.y][pos.x]
    return code


def main():
    exec_tasks(parse_data, task1, task2, read_file('../data/input/year16/day16_02.in'), "95549", "D87AD")


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex(ex)
