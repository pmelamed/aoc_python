import re
from itertools import permutations

from helper import exec_tasks, print_ex, read_file


class Data:
    people_count: int
    relations: dict[tuple[int, int], int]

    def __init__(self, people_count: int, relations: dict[tuple[int, int], int]):
        self.people_count = people_count
        self.relations = relations


def parse_data(lines: list[str]) -> Data:
    names: dict[str, int] = {}
    parsed: dict[tuple[int, int], int] = {}
    matcher = re.compile(r"([A-Za-z]+) would (gain|lose) ([0-9]+) happiness units by sitting next to ([A-Za-z]+).")
    for line in lines:
        matched = matcher.match(line)
        name1 = matched.group(1)
        if name1 in names:
            index1 = names[name1]
        else:
            index1 = len(names)
            names[name1] = index1
        name2 = matched.group(4)
        if name2 in names:
            index2 = names[name2]
        else:
            index2 = len(names)
            names[name2] = index2
        parsed[index1, index2] = int(matched.group(3)) * (1 if matched.group(2) == "gain" else -1)
    return Data(len(names), parsed)


def task1(data: Data) -> int:
    return compute_max_cost(data)


def task2(data: Data) -> int:
    relations: dict[tuple[int, int], int] = dict(data.relations)
    my_index = data.people_count
    for index in range(data.people_count):
        relations.update([((my_index, index), 0) for index in range(data.people_count)])
        relations.update([((index, my_index), 0) for index in range(data.people_count)])
    return compute_max_cost(Data(data.people_count + 1, relations))


def compute_max_cost(data: Data) -> int:
    return max(permutation_cost(perm, data) for perm in permutations(range(data.people_count)))


def permutation_cost(perm: tuple[int, ...], data: Data) -> int:
    return sum(
        data.relations[perm[i], perm[(i + 1) % data.people_count]]
        + data.relations[perm[i], perm[(i + data.people_count - 1) % data.people_count]]
        for i in range(data.people_count))


def main():
    exec_tasks(parse_data, task1, task2, read_file('../data/samples/year15/day15_13.sample'), 330, 286)
    exec_tasks(parse_data, task1, task2, read_file('../data/input/year15/day15_13.in'), 709, 668)


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex(ex)
