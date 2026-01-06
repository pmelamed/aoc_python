import re

import helper
import math_helper
from helper import print_ex, read_file


CMD_PATTERN = re.compile( r"^[^0-9]+([0-9]+)[^0-9]+([0-9]+)[^0-9]+$" )
CODE_FIRST = 20151125
CODE_MULTIPLIER = 252533
CODE_DIVIDER = 33554393

def parse_data( lines: list[ str ] ) -> tuple[ int, int ]:
    match = CMD_PATTERN.match( lines[ 0 ] )
    return int( match.group( 1 ) ), int( match.group( 2 ) )


def task1( data: tuple[ int, int ] ) -> int:
    row, col = data
    number_no = math_helper.progression_sum( 1, row + col - 2, 1 ) + col
    result = CODE_FIRST
    for _ in range( number_no - 1 ):
        result = result * CODE_MULTIPLIER % CODE_DIVIDER
    return result



def main():
    helper.verbose_level = 0
    helper.exec_task(
            parse_data,
            task1,
            read_file( '../data/input/year15/day15_25.in' ),
            2650453
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
