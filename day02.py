import re

import helper


class Data:
    levels = [ ]

    def __init__( self, levels ):
        self.levels = levels


def prepare( lines ):
    levels = [ ]
    for line in lines:
        levels.append( [ int( x ) for x in re.findall( "[0-9]+", line ) ] )
    return Data( levels )


def is_row_safe( levels_row ):
    global_sign = 0
    for index in range( len( levels_row ) - 1 ):
        diff = levels_row[ index ] - levels_row[ index + 1 ]
        if abs( diff ) < 1 or abs( diff ) > 3: return 0
        sign = diff // abs( diff )
        if global_sign != 0 and sign != global_sign: return 0
        global_sign = sign
    return 1


def is_row_safe_ext( levels_row ):
    if is_row_safe( levels_row ): return 1
    for index in range( len( levels_row ) ):
        row_copy = levels_row.copy()
        row_copy.pop( index )
        if is_row_safe( row_copy ): return 1
    return 0


def task1( data ):
    count = 0
    for correct in [ is_row_safe( row ) for row in data.levels ]: count += correct
    return count


def task2( data ):
    count = 0
    for correct in [ is_row_safe_ext( row ) for row in data.levels ]: count += correct
    return count


if __name__ == '__main__':
    try:
        helper.exec_tasks_file( prepare, task1, task2, 'data/day02.sample', 2, 4 )
        helper.exec_tasks_file( prepare, task1, task2, 'data/day02.in', 534, 577 )
    except Exception as ex:
        helper.print_ex( ex )
