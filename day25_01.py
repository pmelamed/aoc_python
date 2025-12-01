from helper import exec_task, print_ex, read_file

type Pattern = tuple[int, int]


class Data:
    turns: list[int]

    def __init__(self, lines: list[str]):
        self.turns = [(-1 if s[0] == 'L' else 1) * int(s[1:]) for s in lines]


def task1(data: Data) -> int:
    pos = 50
    count = 0
    for turn in data.turns:
        pos = (pos + turn % 100 + 100) % 100
        if pos == 0: count += 1
    return count


def task2(data: Data) -> int:
    pos = 50
    count = 0
    for turn in data.turns:
        prev_pos = pos
        pos += turn
        count += abs(pos) // 100
        if prev_pos != 0 and pos <= 0: count += 1
        pos = pos % 100
    return count


def main():
    exec_task(Data, task1, read_file('data/day25_01.sample'), 3)
    exec_task(Data, task1, read_file('data/day25_01.in'), 1129)
    exec_task(Data, task2, read_file('data/day25_01.sample'), 6)
    exec_task(Data, task2, ["L50", "L5", "R10"], 2)
    exec_task(Data, task2, read_file('data/day25_01.in'), 6638)


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex(ex)
