import re
from collections.abc import Iterable

import helper


class Data:
    levels: list[ list[ int ] ]

    def __init__( self, levels: list[ list[ int ] ] ):
        self.levels = levels


def prepare( lines: Iterable[ str ] ) -> Data:
    levels = [ ]
    for line in lines:
        levels.append( [ int( x ) for x in re.findall( "[0-9]+", line ) ] )
    return Data( levels )


def is_row_safe( levels_row: [ int ] ) -> int:
    global_sign = 0
    for index in range( len( levels_row ) - 1 ):
        diff = levels_row[ index ] - levels_row[ index + 1 ]
        if abs( diff ) < 1 or abs( diff ) > 3: return 0
        sign = diff // abs( diff )
        if global_sign != 0 and sign != global_sign: return 0
        global_sign = sign
    return 1


def is_row_safe_ext( levels_row: [ int ] ):
    if is_row_safe( levels_row ): return 1
    for index in range( len( levels_row ) ):
        row_copy = levels_row.copy()
        row_copy.pop( index )
        if is_row_safe( row_copy ): return 1
    return 0


def task1( data: Data ) -> int:
    return sum( [ is_row_safe( row ) for row in data.levels ] )


def task2( data: Data ) -> int:
    return sum( [ is_row_safe_ext( row ) for row in data.levels ] )


def main():
    helper.exec_tasks( prepare, task1, task2, helper.read_file( 'data/day24_02.sample' ), 2, 4 )
    helper.exec_tasks( prepare, task1, task2, helper.read_file( 'data/day24_02.in' ), 534, 577 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        helper.print_ex( ex )
