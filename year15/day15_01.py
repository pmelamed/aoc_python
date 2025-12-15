from helper import exec_tasks, first_line, print_ex, read_file


def task1( data: str ) -> int:
    floor = 0
    for ch in data:
        if ch == '(':
            floor += 1
        else:
            floor -= 1
    return floor


def task2( data: str ) -> int:
    floor = 0
    for idx, ch in enumerate( data ):
        if ch == '(':
            floor += 1
        else:
            floor -= 1
            if floor == -1:
                return idx + 1
    return 0


def main():
    exec_tasks( first_line, task1, task2, read_file( '../data/input/year15/day15_01.in' ), 74, 1795 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
