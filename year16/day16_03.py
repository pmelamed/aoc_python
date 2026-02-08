from geom2d import Coord2D, Rect2D
from helper import exec_tasks, print_ex, read_file

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


def task1(data: list[str]) -> int:
    return sum(is_triangle_possible(*decode_values(line)) for line in data)


def task2(data: list[str]) -> int:
    result = 0
    for line_no in range(0, len(data), 3):
        t1 = decode_values(data[line_no])
        t2 = decode_values(data[line_no + 1])
        t3 = decode_values(data[line_no + 2])
        result += is_triangle_possible(t1[0], t2[0], t3[0])
        result += is_triangle_possible(t1[1], t2[1], t3[1])
        result += is_triangle_possible(t1[2], t2[2], t3[2])
    return result


def decode_values(line: str) -> tuple[int, ...]:
    return tuple(int(s) for s in line.split(" ") if s != "")


def is_triangle_possible(side1: int, side2: int, side3: int) -> int:
    return 1 if (side1 + side2 > side3 and side1 + side3 > side2 and side2 + side3 > side1) else 0


def main():
    exec_tasks(None, task1, task2, read_file('../data/input/year16/day16_03.in'), 983, 1836)


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex(ex)
