from collections import defaultdict
from functools import cmp_to_key

from geom2d import Field2D, STAR_DIRS_2D, Coord2D
from helper import exec_tasks, print_ex, read_file, SYM_OBSTACLE


class Data:
    source: str
    transforms: list[tuple[str, str]]

    def __init__(self, data: list[str]) -> None:
        self.source = data[-1]
        self.transforms = [tuple(line.split(" => ")) for line in data[:-2]]


def task1(data: Data) -> int:
    transformed: set[str] = set()
    for source, transform in data.transforms:
        index = data.source.find(source)
        while index >= 0:
            transformed.add(data.source[:index] + transform + data.source[index + len(source):])
            index = data.source.find(source, index + 1)
    return len(transformed)


def task2(data: Data) -> int:
    transforms = sorted(data.transforms, key=lambda tpl: len(tpl[1]), reverse=True)
    formula = data.source
    steps = 0
    while formula != "e":
        print(f"{steps:>4} -> {formula}")
        for tr_from, tr_to in transforms:
            repl = formula.replace(tr_to, tr_from, 1)
            if repl != formula:
                formula = repl
                steps += 1
                break
        else:
            print(f"Stuck at \'{formula}\'")
            return 0
    return steps


def main():
    exec_tasks(Data, task1, task2, read_file('../data/input/year15/day15_19.in'), 509, None)


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex(ex)
