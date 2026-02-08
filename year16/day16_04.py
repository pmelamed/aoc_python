import re
from collections import Counter
from functools import cmp_to_key

from helper import exec_tasks, print_ex, read_file, exec_task

PARSE_EXP = re.compile(r"([a-z-]+)([0-9]+)\[([a-z]{5})]")


def task1(data: list[str]) -> int:
    return sum(is_room_real(line) for line in data)


def task2(data: list[str]) -> int:
    return [sector_id for name, sector_id in [decode_line(line) for line in data] if name.find("northpole") >= 0][0]


def is_room_real(line: str) -> int:
    m = PARSE_EXP.match(line)
    return int(m.group(2)) if calc_checksum(m.group(1)) == m.group(3) else 0


def calc_checksum(line: str) -> str:
    cnt = Counter([c for c in line if c != '-'])
    result = [(letter, count) for letter, count in cnt.items()]
    result.sort(key=cmp_to_key(compare_letters))
    return "".join([letter for letter, _ in result[:5]])


def compare_letters(a: tuple[str, int], b: tuple[str, int]) -> int:
    return ord(a[0]) - ord(b[0]) if a[1] == b[1] else b[1] - a[1]


def decode_line(line: str) -> tuple[str, int]:
    m = PARSE_EXP.match(line)
    sector_id = int(m.group(2))
    return "".join(rotate_char(ch, sector_id) for ch in m.group(1)), sector_id


def rotate_char(ch: str, steps: int) -> str:
    return chr((ord(ch) - ord('a') + steps) % 26 + ord('a')) if ch != '-' else ' '


def main():
    sample = [
        "aaaaa-bbb-z-y-x-123[abxyz]",
        "a-b-c-d-e-g--h-987[abcde]",
        "not-a-real-room-404[oarel]",
        "totally-real-room-200[decoy]"
    ]
    exec_task(None, task1, sample, 1514)
    exec_tasks(None, task1, task2, read_file('../data/input/year16/day16_04.in'), 409147, 991)


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex(ex)
