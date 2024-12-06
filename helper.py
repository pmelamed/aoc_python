import sys
import traceback
from collections.abc import Callable, Iterable

CROSS_DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))
X_DIRS = ((1, -1), (1, 1), (-1, 1), (-1, -1))
STAR_DIRS = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))


def task_check[ DataT, ResultT: str | int ]( func: Callable[ [ DataT ], ResultT ] | None,
                                             data: DataT,
                                             sample: ResultT ):
    result = func( data )
    if sample is None:
        print( f"\x1b[1;5;30;100m RESULT \x1b[0m - {result}" )
    else:
        if result == sample:
            print( f"\x1b[1;5;30;42m   OK   \x1b[0m - {result} == {sample}" )
        else:
            print( f"\x1b[1;5;30;41m  FAIL  \x1b[0m - {result} != {sample}" )


def exec_tasks[ DataT, ResultT1: str | int, ResultT2: str | int ](
        prepare_fn: Callable[ [ Iterable[ str ] ], DataT ] | None,
        task1_fn: Callable[ [ DataT ], ResultT1 ],
        task2_fn: Callable[ [ DataT ], ResultT2 ],
        data: Iterable[ str ] | DataT,
        check_value1: ResultT1 | None,
        check_value2: ResultT2 | None ):
    if prepare_fn is not None:
        data = prepare_fn( data )
    task_check( task1_fn, data, check_value1 )
    task_check( task2_fn, data, check_value2 )


def exec_task[ DataT, ResultT: str | int ](
        prepare_fn: Callable[ [ Iterable[ str ] ], DataT ] | None,
        task_fn: Callable[ [ DataT ], ResultT ],
        data: Iterable[ str ] | DataT,
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


def turn_right( d: tuple[ int, int ] ) -> tuple[ int, int ]:
    return -d[ 1 ], d[ 0 ]


def turn_left( d: tuple[ int, int ] ) -> tuple[ int, int ]:
    return d[ 1 ], -d[ 0 ]


def count_if[ T ]( condition: Callable[ [ T ], bool ], seq: Iterable[ T ] ) -> int:
    return sum( [ 1 for obj in seq if condition( obj ) ] )
