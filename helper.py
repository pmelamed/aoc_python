import datetime
import sys
import traceback
from collections.abc import Callable, Iterable
from typing import TypeAlias

Coord: TypeAlias = tuple[ int, int ]
Direction: TypeAlias = tuple[ int, int ]
Rect: TypeAlias = tuple[ int, int, int, int ]

CROSS_DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))
X_DIRS = ((1, -1), (1, 1), (-1, 1), (-1, -1))
STAR_DIRS = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))


def task_check[ DataT, ResultT: str | int ]( func: Callable[ [ DataT ], ResultT ] | None,
                                             data: DataT,
                                             sample: ResultT ):
    start = datetime.datetime.now( datetime.timezone.utc )
    result = func( data )
    delta = int( (datetime.datetime.now( datetime.timezone.utc ) - start).total_seconds() * 1000 )
    if sample is None:
        print( f"\x1b[1;5;30;100m RESULT \x1b[0m - {result} \u231B {delta}" )
    else:
        if result == sample:
            print( f"\x1b[1;5;30;42m   OK   \x1b[0m - {result} \u231B {delta}" )
        else:
            print( f"\x1b[1;5;30;41m  FAIL  \x1b[0m - {result} != {sample}" )


def exec_tasks[ DataT, ResultT1: str | int, ResultT2: str | int ](
        prepare_fn: Callable[ [ list[ str ] ], DataT ] | None,
        task1_fn: Callable[ [ DataT ], ResultT1 ],
        task2_fn: Callable[ [ DataT ], ResultT2 ],
        data: list[ str ] | DataT,
        check_value1: ResultT1 | None,
        check_value2: ResultT2 | None ):
    if prepare_fn is not None:
        data = prepare_fn( data )
    task_check( task1_fn, data, check_value1 )
    task_check( task2_fn, data, check_value2 )


def exec_task[ DataT, ResultT: str | int ](
        prepare_fn: Callable[ [ list[ str ] ], DataT ] | None,
        task_fn: Callable[ [ DataT ], ResultT ],
        data: list[ str ] | DataT,
        check_value: ResultT | None ):
    if prepare_fn is not None:
        data = prepare_fn( data )
    task_check( task_fn, data, check_value )


def read_file( file_name: str ) -> list[ str ]:
    with open( file_name ) as file:
        return [ line[ :-1 ] if line[ -1: ] == "\n" else line for line in file.readlines() ]


def print_ex( ex: Exception ):
    [ print( line, file=sys.stderr ) for line in traceback.format_exception( ex ) ]


def not_empty_str_predicate( s ):
    return s != ""


def turn_cw90( d: tuple[ int, int ] ) -> tuple[ int, int ]:
    return -d[ 1 ], d[ 0 ]


def turn_ccw90( d: tuple[ int, int ] ) -> tuple[ int, int ]:
    return d[ 1 ], -d[ 0 ]


def move_forward( pos: tuple[ int, int ], direction: tuple[ int, int ] ) -> tuple[ int, int ]:
    return pos[ 0 ] + direction[ 0 ], pos[ 1 ] + direction[ 1 ]


def move_backward( pos: tuple[ int, int ], direction: tuple[ int, int ] ) -> tuple[ int, int ]:
    return pos[ 0 ] - direction[ 0 ], pos[ 1 ] - direction[ 1 ]


def inside_rect( pos: tuple[ int, int ], rect: tuple[ int, int, int, int ] ) -> bool:
    return rect[ 0 ] <= pos[ 0 ] < rect[ 2 ] and rect[ 1 ] <= pos[ 1 ] < rect[ 3 ]


def count_if[ T ]( condition: Callable[ [ T ], bool ], seq: Iterable[ T ] ) -> int:
    return sum( [ 1 for obj in seq if condition( obj ) ] )


def coord_add( p1: Coord, p2: Coord ) -> Coord:
    return p1[ 0 ] + p2[ 0 ], p1[ 1 ] + p2[ 1 ]


def coord_sub( p1: Coord, p2: Coord ) -> Coord:
    return p1[ 0 ] - p2[ 0 ], p1[ 1 ] - p2[ 1 ]


def field_rect( width: int, height: int ) -> Rect:
    return 0, 0, width, height
