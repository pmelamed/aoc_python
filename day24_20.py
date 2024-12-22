import functools
from collections import defaultdict
from typing import Optional

from helper import Coord, CROSS_DIRS, exec_tasks, Field, field_from_input, move_forward, print_ex, read_file

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
    way.append( end )
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
    for index_start, pt_start in enumerate( data.way[ :-min_save ] ):
        for index_end, pt_end in enumerate( data.way[ index_start + min_save: ] ):
            cheat_length = find_cheat( data.field, pt_start, pt_end )
            if cheat_length is not None:
                cheats[ index_end - index_start - cheat_length ] += 1
    return sum( v for l, v in cheats.items() if l >= min_save )


def find_cheat(field: Field[int], pt_start: Coord, pt_end: Coord ) -> Optional[int]:
    wave = [pt_start]
    pass

def main():
    exec_tasks(
        prepare,
        functools.partial( task1, min_save = 10 ),
        functools.partial( task2, min_save = 10 ),
        read_file( 'data/day24_20.sample' ),
        10,
        305
    )
    exec_tasks(
        prepare,
        functools.partial( task1, min_save = 100 ),
        functools.partial( task2, min_save = 100 ),
        read_file( 'data/day24_20.in' ),
        1441,
        None
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
