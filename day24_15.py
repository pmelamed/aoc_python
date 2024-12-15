from typing import Callable

from helper import print_ex, Coord, exec_tasks, Field, field_from_input, move_forward, move_backward, exec_task
from helper import read_file

type Data = tuple[ Field[ int ], str, Coord ]

BOX = ord( 'O' )
LBOX = ord( '[' )
RBOX = ord( ']' )
OBSTACLE = ord( '#' )
ROBOT = ord( '@' )
EMPTY = ord( '.' )

DIRS = { ">": (1, 0), "<": (-1, 0), "v": (0, 1), "^": (0, -1) }
WIDE_CHAR = { ".": "..", "O": "[]", "#": "##", "@": "@." }


def prepare( lines: list[ str ], field_line_t: Callable[ [ str ], str ] = lambda s: s ) -> Data:
    split_index = lines.index( "" )
    field = field_from_input( [ field_line_t( line ) for line in lines[ :split_index ] ] )
    robot = field.find( lambda _1, _2, v, _3: v == ROBOT )
    field[ robot ] = EMPTY
    return field, "".join( lines[ split_index + 1: ] ), robot


def task1( data: list[ str ] ) -> int:
    field, moves, robot = prepare( data )
    for move in map( DIRS.get, moves ):
        pt = move_forward( robot, move )
        count = 0
        while field[ pt ] == BOX:
            pt = move_forward( pt, move )
            count += 1
        if field[ pt ] == EMPTY:
            for _ in range( count ):
                field[ pt ] = BOX
                pt = move_backward( pt, move )
            robot = pt
            field[ pt ] = EMPTY
    return sum( gps_coord( x, y ) for x, y, _ in field.filter( lambda x, y, v, _: v == BOX ) )


def task2( data: list[ str ] ) -> int:
    field, moves, robot = prepare( data, widen_line )
    for move in map( DIRS.get, moves ):
        pass
    return sum( gps_coord( x, y ) for x, y, _ in field.filter( lambda x, y, v, _: v == LBOX ) )


def gps_coord( x: int, y: int ) -> int:
    return 100 * y + x


def widen_line( line: str ) -> str:
    try:
        return "".join( WIDE_CHAR.get( ch ) for ch in line )
    except Exception as ex:
        for ch in line: print( f"<{ch}>" )
        raise ex


def main():
    exec_task( None, task1, read_file( 'data/day24_15_2.sample' ), 2028 )
    exec_tasks( None, task1, task2, read_file( 'data/day24_15_1.sample' ), 10092, 9021 )
    exec_tasks( None, task1, task2, read_file( 'data/day24_15.in' ), 1371036, None )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
