import hashlib

from helper import exec_tasks, first_line, print_ex, read_file


def task1( data: str ) -> int:
    result = 0
    while hashlib.md5( (data + str( result )).encode( "utf-8" ) ).hexdigest()[ 0:5 ] != "00000":
        result += 1
    return result


def task2( data: str ) -> int:
    result = 0
    while hashlib.md5( (data + str( result )).encode( "utf-8" ) ).hexdigest()[ 0:6 ] != "000000":
        result += 1
    return result


def main():
    exec_tasks( first_line, task1, task2, read_file( '../data/input/year15/day15_04.in' ), 346386, 9958218 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
