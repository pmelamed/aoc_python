from helper import exec_tasks, print_ex, read_file


def task1( lines: list[ str ] ) -> int:
    return sum( line_diff( line ) for line in lines )


def task2( lines: list[ str ] ) -> int:
    return sum( encoded_diff( line ) for line in lines )


def line_diff( line: str ) -> int:
    count = 2
    idx = 1
    while idx < len( line ) - 1:
        if line[ idx ] == "\\":
            if line[ idx + 1 ] == "x":
                idx += 3
                count += 3
            else:
                idx += 1
                count += 1
        idx += 1
    return count


def encoded_diff( line: str ) -> int:
    return 2 + sum( 1 if c in "\"\\" else 0 for c in line )


def main():
    exec_tasks( None, task1, task2, read_file( '../data/input/year15/day15_08.in' ), 1371, 2117 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
