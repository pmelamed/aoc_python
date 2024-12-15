from typing import Callable

from helper import print_ex, Coord, exec_tasks, Field, field_from_input, move_forward, move_backward, exec_task, \
    Direction
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
    field, moves, robot = prepare( data, lambda s: "".join( WIDE_CHAR.get( ch ) for ch in s ) )
    for move in map( DIRS.get, moves ):
        if move[ 0 ] != 0:
            robot = move_horizontally( field, move, robot )
        else:
            robot = move_vertically( field, move, robot )
    return sum( gps_coord( x, y ) for x, y, _ in field.filter( lambda x, y, v, _: v == LBOX ) )


def gps_coord( x: int, y: int ) -> int:
    return 100 * y + x


def move_horizontally( field: Field[ int ], move: Direction, robot: Coord ) -> Coord:
    pt = move_forward( robot, move )
    count = 0
    while field[ pt ] in (LBOX, RBOX):
        pt = move_forward( pt, move )
        count += 1
    if field[ pt ] == EMPTY:
        for _ in range( count ):
            npt = move_backward( pt, move )
            field[ pt ] = field[ npt ]
            pt = npt
        field[ pt ] = EMPTY
        return pt
    return robot


def move_vertically( field: Field[ int ], move: Direction, robot: Coord ) -> Coord:
    pt = move_forward( robot, move )
    cell = field[ pt ]
    if cell == OBSTACLE: return robot
    if cell == EMPTY: return pt
    if cell == LBOX: return pt if move_box_vertically( field, move, pt ) else robot
    if cell == RBOX: return pt if move_box_vertically( field, move, move_forward( pt, (-1, 0) ) ) else robot


def move_box_vertically( field: Field[ int ], move: Direction, box: Coord ) -> bool:
    points: dict[ Coord, int ] = dict()
    if scan_box_vertically( field, move, box, points ):
        for pt in points.keys(): field[ pt ] = EMPTY
        for pt, side in points.items():
            field[ move_forward( pt, move ) ] = side
        return True
    return False


def scan_box_vertically( field: Field[ int ], move: Direction, lbox: Coord, points: dict[ Coord, int ] ) -> bool:
    rbox = move_forward( lbox, (1, 0) )
    points[ lbox ] = LBOX
    points[ rbox ] = RBOX
    nlbox = move_forward( lbox, move )
    nrbox = move_forward( rbox, move )
    nlcell = field[ nlbox ]
    nrcell = field[ nrbox ]
    if nlcell == OBSTACLE or nrcell == OBSTACLE: return False
    if nlcell == LBOX: return scan_box_vertically( field, move, nlbox, points )
    rscan = True
    if nrcell == LBOX:
        rscan = scan_box_vertically( field, move, nrbox, points )
        if nlcell == EMPTY: return rscan
    if nlcell == RBOX:
        lscan = scan_box_vertically( field, move, move_forward( nlbox, (-1, 0) ), points )
        if nrcell == EMPTY:
            return lscan
        else:
            return lscan and rscan
    return True


def main():
    exec_task( None, task1, read_file( 'data/day24_15_2.sample' ), 2028 )
    exec_tasks( None, task1, task2, read_file( 'data/day24_15_1.sample' ), 10092, 9021 )
    exec_tasks( None, task1, task2, read_file( 'data/day24_15.in' ), 1371036, 1392847 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
