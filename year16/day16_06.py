from collections import Counter

from helper import exec_tasks, read_file, print_ex


def task1(data: list[str]) -> str:
    msg_len = len(data[0])
    return "".join([Counter([l[index] for l in data]).most_common()[0][0] for index in range(msg_len)])


def task2(data: list[str]) -> str:
    msg_len = len(data[0])
    return "".join([Counter([l[index] for l in data]).most_common()[-1][0] for index in range(msg_len)])


def main():
    exec_tasks(None, task1, task2, read_file('../data/input/year16/day16_06.in'), "mlncjgdg", "bipjaytb")


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex(ex)
