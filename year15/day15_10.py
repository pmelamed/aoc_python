from helper import exec_tasks, first_line, print_ex, read_file


def task1( data: str ) -> int:
    result = data
    for _ in range( 40 ):
        result = encode_str( result )
    return len( result )


def task2( data: str ) -> int:
    result = data
    for _ in range( 50 ):
        result = encode_str( result )
    return len( result )


def encode_str( line: str ) -> str:
    result = ""
    ch = line[ 0 ]
    length = 1
    for nch in line[ 1: ]:
        if nch == ch:
            length += 1
        else:
            result += f"{length}{ch}"
            ch = nch
            length = 1
    return result + f"{length}{ch}"


def main():
    exec_tasks( first_line, task1, task2, read_file( '../data/input/year15/day15_10.in' ), 360154, 5103798 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
