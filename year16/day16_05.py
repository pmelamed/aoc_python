import hashlib

from helper import exec_tasks, print_ex, read_file, first_line


def task1(door_id: str) -> str:
    pwd = ""
    index = 0
    while len(pwd) < 8:
        door_hash = hashlib.md5((door_id + str(index)).encode("utf-8")).hexdigest()
        if door_hash.startswith("00000"):
            pwd += door_hash[5]
        index += 1
    return pwd


def task2(door_id: str) -> str:
    pwd = 8 * [' ']
    filled = 0
    index = 0
    while filled < 8:
        door_hash = hashlib.md5((door_id + str(index)).encode("utf-8")).hexdigest()
        if door_hash.startswith("00000"):
            pos = ord(door_hash[5]) - ord('0')
            if pos < 8 and pwd[pos] == ' ':
                pwd[pos] = door_hash[6]
                filled += 1
        index += 1
    return "".join(pwd)


def main():
    exec_tasks(first_line, task1, task2, read_file('../data/input/year16/day16_05.in'), "c6697b55", "8c35d1ab")


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex(ex)
