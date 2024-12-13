import itertools
import re

from helper import exec_tasks, print_ex
from helper import read_file

type Case = tuple[ int, int, int, int, int, int ]
type Data = list[ Case ]


def prepare( lines: list[ str ] ) -> Data:
    return [ parse_case( case ) for case in itertools.batched( [ line for line in lines if len( line ) != 0 ], 3 ) ]


def task1( data: Data ) -> int:
    return sum( play_case( case ) for case in data )


def task2( data: Data ) -> int:
    return 0


def parse_case( lines: tuple[ str, ... ] ) -> Case:
    try:
        fa = re.findall( r"Button A: X\+([0-9]+), Y\+([0-9]+)", lines[ 0 ] )[ 0 ]
        fb = re.findall( r"Button B: X\+([0-9]+), Y\+([0-9]+)", lines[ 1 ] )[ 0 ]
        fp = re.findall( r"Prize: X=([0-9]+), Y=([0-9]+)", lines[ 2 ] )[ 0 ]
    except Exception as x:
        print( lines )
        raise IndexError( f"Lines = {lines} Ex: {x}" )
    try:
        return int( fa[ 0 ] ), int( fa[ 1 ] ), int( fb[ 0 ] ), int( fb[ 1 ] ), int( fp[ 0 ] ), int( fp[ 1 ] )
    except Exception as x:
        print( lines )
        raise IndexError( f"Lines = {lines} Parsed = {fa}, {fb}, {fp} Ex: {ex}" )


def get_case_price( a_count: int, case: Case ) -> int:
    x_div, x_mod = divmod( (case[ 4 ] - a_count * case[ 0 ]), case[ 2 ] )
    y_div, y_mod = divmod( case[ 5 ] - a_count * case[ 1 ], case[ 3 ] )
    return a_count * 3 + x_div if x_mod == 0 and y_mod == 0 and x_div == y_div else 0


def play_case( case: Case ) -> int:
    result = 0
    a_count = 0
    while a_count < 100 and case[ 0 ] * a_count <= case[ 4 ] and case[ 1 ] * a_count <= case[ 5 ]:
        price = get_case_price( a_count, case )
        if price != 0: result = price if result == 0 else min( price, result )
        a_count += 1
    return result


def main():
    exec_tasks( prepare, task1, task2, read_file( 'data/day24_13.sample' ), 480, None )
    exec_tasks( prepare, task1, task2, read_file( 'data/day24_13.in' ), None, None )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
