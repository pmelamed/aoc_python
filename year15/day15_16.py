import operator
from collections import defaultdict
from typing import Callable

from helper import exec_tasks, print_ex, read_file

type Aunt = dict[str, int]

type Data = list[Aunt]

type MatchFunctions = dict[str, Callable[[int, int], bool]]


def parse_data(lines: list[str]) -> Data:
    return [parse_aunt(line[line.index(": ") + 2:]) for line in lines]


def parse_aunt(line: str) -> Aunt:
    return dict(parse_item(item) for item in line.split(", "))


def parse_item(item: str) -> tuple[str, int]:
    name, val = item.split(": ", 2)
    return name, int(val)


SAMPLE = parse_aunt(
    "children: 3, cats: 7, samoyeds: 2, pomeranians: 3, akitas: 0, "
    "vizslas: 0, goldfish: 5, trees: 3, cars: 2, perfumes: 1"
)


def task1(data: Data) -> int:
    return match_aunts(data, defaultdict(lambda: operator.eq))


def task2(data: Data) -> int:
    match_fn: MatchFunctions = defaultdict(lambda: operator.eq)
    match_fn.update({
        "cats": operator.gt,
        "trees": operator.gt,
        "pomeranians": operator.lt,
        "goldfish": operator.lt
    })
    return match_aunts(data, match_fn)


def match_aunts(data: list[dict[str, int]], match_fn: MatchFunctions) -> int:
    for index, aunt in enumerate(data):
        if match_aunt(aunt, SAMPLE, match_fn):
            return index + 1
    return -1


def match_aunt(aunt: Aunt, sample: Aunt, match_fn: MatchFunctions) -> bool:
    for k in aunt.keys():
        if k in sample and not match_fn[k](aunt[k], sample[k]):
            return False
    return True


def main():
    exec_tasks(parse_data, task1, task2, read_file('../data/input/year15/day15_16.in'), 373, 260)


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex(ex)
