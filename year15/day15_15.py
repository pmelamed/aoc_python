import functools
import itertools
import operator
import re
from itertools import permutations
from typing import Callable
from xml.sax.handler import property_encoding

from helper import exec_tasks, print_ex, read_file

PARSE_MATCHER = re.compile(r"([A-Za-z]+): capacity (-?[0-9]+), durability (-?[0-9]+), flavor (-?[0-9]+), "
                           r"texture (-?[0-9]+), calories (-?[0-9]+)")

type Ingredient = tuple[int, int, int, int, int]

type Data = list[Ingredient]


def parse_data(lines: list[str]) -> Data:
    return [parse_ingredient(line) for line in lines]


def parse_ingredient(line: str) -> Ingredient:
    matched = PARSE_MATCHER.match(line)
    return (
        int(matched.group(2)),
        int(matched.group(3)),
        int(matched.group(4)),
        int(matched.group(5)),
        int(matched.group(6))
    )


def task1(data: Data) -> int:
    return iterate_ingredient(data,
                              0,
                              100,
                              len(data) * [0],
                              lambda _d, _q: True)


def task2(data: Data) -> int:
    return iterate_ingredient(data,
                              0,
                              100,
                              len(data) * [0],
                              lambda d, q: compute_cookie_property(d, 4, q) == 500)


def iterate_ingredient(data: Data,
                       ingredient_index: int,
                       rest: int,
                       quantities: list[int],
                       calories_checker: Callable[[Data, list[int]], bool]) -> int:
    if ingredient_index == len(data) - 1:
        quantities[ingredient_index] = rest
        return compute_cookie_rate(data, quantities) if calories_checker(data, quantities) else 0
    result: int = 0
    for quantity in range(rest - (len(data) - 1 - ingredient_index)):
        quantities[ingredient_index] = quantity
        result = max(result,
                     iterate_ingredient(data, ingredient_index + 1, rest - quantity, quantities, calories_checker))
    return result


def compute_cookie_rate(data: Data, quantities: list[int]) -> int:
    return functools.reduce(
        operator.mul,
        [compute_cookie_property(data, property_index, quantities) for property_index in range(4)],
        1
    )


def compute_cookie_property(data: Data, property_index: int, quantities: list[int]) -> int:
    return max(
        0,
        sum(data[ingredient_index][property_index] * quantity for ingredient_index, quantity in enumerate(quantities))
    )


def main():
    exec_tasks(parse_data, task1, task2, read_file('../data/samples/year15/day15_15.sample'), 62842880, 57600000)
    exec_tasks(parse_data, task1, task2, read_file('../data/input/year15/day15_15.in'), 21367368, 1766400)


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex(ex)
