import functools
from collections import defaultdict

from helper import (
    CROSS_DIRS, Coord, Field, exec_tasks, field_from_input, manhattan, move_forward, print_ex, read_file
)


EMPTY = ord( "." )
OBSTACLE = ord( "#" )
PASSED = ord( "x" )
START = ord( "S" )
END = ord( "E" )
DOUBLE_CROSS_DIR = ((2, 0), (-2, 0), (0, 2), (0, -2))


class Data:
    field: Field[ int ]
    way: list[ Coord ]

    def __init__(
            self,
            field: Field[ int ],
            way: list[ Coord ]
    ):
        self.field = field
        self.way = way


def prepare( lines: list[ str ] ) -> Data:
    field = field_from_input( lines )
    start = field.find( lambda _x, _y, v, _f: v == START )
    end = field.find( lambda _x, _y, v, _f: v == END )
    field[ end ] = EMPTY
    way = [ start ]
    while start != end:
        for d in CROSS_DIRS:
            pt = move_forward( start, d )
            if field[ pt ] == EMPTY:
                way.append( pt )
                start = pt
                field[ start ] = PASSED
                break
    return Data( field, way )


def task1( data: Data, min_save: int ) -> int:
    cheats = defaultdict( lambda: 0 )
    for index in range( len( data.way ) ):
        way_pt = data.way[ index ]
        for d in DOUBLE_CROSS_DIR:
            pt = move_forward( way_pt, d )
            if pt in data.field and data.field[ pt ] == PASSED:
                cheat_size = data.way.index( pt ) - index - 2
                cheats[ cheat_size ] += 1
    return sum( v for l, v in cheats.items() if l >= min_save )


def task2( data: Data, min_save: int ) -> int:
    cheats = defaultdict( lambda: 0 )
    way_length = len( data.way )
    for index_start in range( way_length - min_save ):
        for index_end in range( index_start + min_save, way_length ):
            cheat_length = manhattan( data.way[ index_start ], data.way[ index_end ] )
            if cheat_length <= 20:
                cheats[ index_end - index_start - cheat_length ] += 1
    return sum( v for l, v in cheats.items() if l >= min_save )


def main():
    exec_tasks(
            prepare,
            functools.partial( task1, min_save = 10 ),
            functools.partial( task2, min_save = 50 ),
            read_file( 'data/day24_20.sample' ),
            10,
            285
    )
    exec_tasks(
            prepare,
            functools.partial( task1, min_save = 100 ),
            functools.partial( task2, min_save = 100 ),
            read_file( 'data/day24_20.in' ),
            1441,
            1021490
    )


# N < 43535613

if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
