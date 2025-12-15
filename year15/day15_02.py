import functools
import operator

from helper import exec_tasks, print_ex, read_file


type Data = tuple[ tuple[ int, ... ], ... ]


def parse_data( lines: list[ str ] ) -> Data:
    return tuple( tuple( int( s ) for s in line.split( "x" ) ) for line in lines )


def task1( data: Data ) -> int:
    return sum( present_wrapper_square( present ) for present in data )


def task2( data: Data ) -> int:
    return sum( present_ribbon_length( present ) for present in data )


def present_wrapper_square( present: tuple[ int, ... ] ) -> int:
    side1 = present[ 0 ] * present[ 1 ]
    side2 = present[ 0 ] * present[ 2 ]
    side3 = present[ 2 ] * present[ 1 ]
    return (side1 + side2 + side3) * 2 + min( side1, side2, side3 )


def present_ribbon_length( present: tuple[ int, ... ] ) -> int:
    return (sum( present ) - max( present )) * 2 + functools.reduce( operator.mul, present, 1 )


def main():
    exec_tasks( parse_data, task1, task2, read_file( '../data/input/year15/day15_02.in' ), 1586300, 3737498 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
