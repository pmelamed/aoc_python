import functools
import operator

from helper import exec_tasks, first_line, print_ex, read_file


ALLOWED_CHARS = "abcdefghjkmnpqrstuvwxyz"
ALLOWED_CHARS_COUNT = len( ALLOWED_CHARS )


def task1( data: str ) -> str:
    password = [ ALLOWED_CHARS.index( ch ) for ch in data ]
    password = increment_password( password )
    while not (check_straight_rule( password ) and check_pairs_rule( password )):
        password = increment_password( password )
    return functools.reduce( operator.add, [ ALLOWED_CHARS[ index ] for index in password ], "" )


def task2( data: str ) -> str:
    return task1( task1( data ) )


def increment_password( password: list[ int ] ) -> list[ int ]:
    index = len( password ) - 1
    password[ index ] += 1
    while index >= 0 and password[ index ] == ALLOWED_CHARS_COUNT:
        password[ index ] = 0
        index -= 1
        password[ index ] += 1
    return password


def check_straight_rule( password: list[ int ] ) -> bool:
    for index in range( len( password ) - 3 ):
        if password[ index ] + 1 == password[ index + 1 ] and password[ index ] + 2 == password[ index + 2 ]:
            return True
    else:
        return False


def check_pairs_rule( password: list[ int ] ) -> bool:
    pair_met = -1
    index = 1
    while index < len( password ):
        if password[ index ] == password[ index - 1 ]:
            if pair_met == -1:
                pair_met = password[ index ]
            elif pair_met != password[ index ]:
                return True
            index += 1
        index += 1
    return False


def main():
    exec_tasks( first_line, task1, task2, read_file( '../data/input/year15/day15_11.in' ), "cqjxxyzz", "cqkaabcc" )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
