from helper import exec_tasks, print_ex, read_file

SAMPLE_DATA = ["20", "15", "10", "5", "5"]


def parse_data(lines: list[str]) -> list[int]:
    return sorted([int(line) for line in lines], reverse=True)


def task1(data: list[int], to_fit: int) -> int:
    return place_eggnog(data, 0, to_fit)


def task2(data: list[int], to_fit: int) -> int:
    min_required = find_min_required(data, 0, to_fit)
    return place_eggnog_fixed(data, 0, to_fit, 0, min_required)


def place_eggnog(containers: list[int], container_idx: int, rest: int) -> int:
    if rest == 0:
        return 1
    return sum(place_eggnog(containers, used_idx + 1, rest - containers[used_idx])
               for used_idx in range(container_idx, len(containers))
               if containers[used_idx] <= rest)


def place_eggnog_fixed(containers: list[int],
                       container_idx: int,
                       rest: int,
                       used_count: int,
                       expected_count: int) -> int:
    if used_count == expected_count:
        return 1 if rest == 0 else 0
    return sum(place_eggnog_fixed(containers, used_idx + 1, rest - containers[used_idx], used_count + 1, expected_count)
               for used_idx in range(container_idx, len(containers))
               if containers[used_idx] <= rest)


def find_min_required(containers: list[int], container_idx: int, rest: int) -> int:
    if rest == 0:
        return 0
    if rest < 0 or container_idx == len(containers):
        return len(containers) + 1
    return 1 + min(find_min_required(containers, used_idx + 1, rest - containers[used_idx])
                   for used_idx in range(container_idx, len(containers)))


def main():
    exec_tasks(parse_data,
               lambda d: task1(d, 25),
               lambda d: task2(d, 25),
               SAMPLE_DATA,
               4,
               3)
    exec_tasks(parse_data,
               lambda d: task1(d, 150),
               lambda d: task2(d, 150),
               read_file('../data/input/year15/day15_17.in'),
               654,
               57)


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex(ex)
