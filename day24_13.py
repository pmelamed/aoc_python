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
    return sum( play_case( (ax, ay, bx, by, px + 10000000000000, py + 10000000000000) )
                for ax, ay, bx, by, px, py in data )


def parse_case( lines: tuple[ str, ... ] ) -> Case:
    fa = re.findall( r"Button A: X\+([0-9]+), Y\+([0-9]+)", lines[ 0 ] )[ 0 ]
    fb = re.findall( r"Button B: X\+([0-9]+), Y\+([0-9]+)", lines[ 1 ] )[ 0 ]
    fp = re.findall( r"Prize: X=([0-9]+), Y=([0-9]+)", lines[ 2 ] )[ 0 ]
    return int( fa[ 0 ] ), int( fa[ 1 ] ), int( fb[ 0 ] ), int( fb[ 1 ] ), int( fp[ 0 ] ), int( fp[ 1 ] )


def play_case( case: Case ) -> int:
    ax, ay, bx, by, px, py = case
    an = (py * bx - px * by) / (ay * bx - ax * by)
    if an.is_integer():
        bn = (px - an * ax) / bx
        if bn.is_integer():
            return int( 3 * an + bn )
    return 0


def main():
    exec_tasks( prepare, task1, task2, read_file( 'data/day24_13.sample' ), 480, 875318608908 )
    exec_tasks( prepare, task1, task2, read_file( 'data/day24_13.in' ), 34787, 85644161121698 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
