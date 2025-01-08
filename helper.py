import datetime
import sys
import traceback
from collections.abc import Callable, Iterable
from typing import Any, Optional

type Coord = tuple[ int, int ]
type Direction = tuple[ int, int ]
type Rect = tuple[ int, int, int, int ]

CROSS_DIRS = ((0, -1), (1, 0), (0, 1), (-1, 0))
X_DIRS = ((1, -1), (1, 1), (-1, 1), (-1, -1))
STAR_DIRS = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))

SYM_DIRS = {
    ord( ">" ): (1, 0),
    ord( "<" ): (-1, 0),
    ord( "^" ): (0, -1),
    ord( "v" ): (0, 1)
}

SYM_OBSTACLE = ord( "#" )
SYM_PLANE = ord( "." )
SYM_START = ord( "S" )
SYM_END = ord( "E" )


class Field[ DataT ]:
    cells: list[ list[ DataT ] ]
    height: int
    width: int

    def __init__( self, width: int, height: int, cells: list[ list[ DataT ] ] ):
        self.width = width
        self.height = height
        self.cells = cells

    def __getitem__( self, item: Coord ) -> DataT:
        return self.cells[ item[ 1 ] ][ item[ 0 ] ]

    def __setitem__( self, item: Coord, v: DataT ) -> DataT:
        self.cells[ item[ 1 ] ][ item[ 0 ] ] = v
        return v

    def __contains__( self, item: Coord ):
        return self.contains( item )

    def copy( self ):
        return Field( self.width, self.height, [ line.copy() for line in self.cells ] )

    def contains( self, pt: Coord ):
        return 0 <= pt[ 0 ] < self.width and 0 <= pt[ 1 ] < self.height

    def filter( self,
                filter_fn: Callable[ [ int, int, DataT, Any ], bool ] ) -> Iterable[ tuple[ int, int, DataT ] ]:
        return FieldFilterIterator( self, filter_fn )

    def find( self, filter_fn: Callable[ [ int, int, DataT, Any ], bool ] ) -> Optional[ Coord ]:
        for y in range( self.height ):
            for x in range( self.width ):
                if filter_fn( x, y, self.cells[ y ][ x ], self ): return x, y
        return None

    def dump( self,
              cell_str_f: Callable[ [ int, int, DataT ], str ] = lambda x, y, cell: str( cell ),
              delim: str = " " ) -> str:
        strs = [ [ cell_str_f( x, y, self.cells[ y ][ x ] ) for x in range( self.width ) ]
                 for y in range( self.height ) ]
        cell_width = max( max( len( cell ) for cell in line ) for line in strs )
        return "\n".join( delim.join( cell.rjust( cell_width, " " ) for cell in line ) for line in strs )


class FieldFilterIterator[ DataT ]:
    x: int
    y: int
    field: Field[ DataT ]
    filter_fn: Callable[ [ int, int, DataT, Field[ DataT ] ], bool ]

    def __init__(
        self,
        field: Field[ DataT ],
        filter_fn: Callable[ [ int, int, DataT, Field[ DataT ] ], bool ]
    ):
        self.field = field
        self.filter_fn = filter_fn
        self.x = self.y = 0
        pass

    def __iter__( self ):
        self.x = self.y = 0
        return self

    def __next__( self ) -> tuple[ int, int, DataT ]:
        while self.y < self.field.height:
            while self.x < self.field.width:
                if self.filter_fn( self.x, self.y, self.field.cells[ self.y ][ self.x ], self.field ):
                    self.x += 1
                    return self.x - 1, self.y, self.field.cells[ self.y ][ self.x - 1 ]
                self.x += 1
            self.x = 0
            self.y += 1
        raise StopIteration()


def field_from_input[ DataT, RawCellT ](
    lines: Iterable[ str ],
    /, *,
    line_filter: Callable[ [ str ], bool ] = lambda s: True,
    line_t: Callable[ [ str ], list[ RawCellT ] ] =
    lambda s: [ c for c in bytes( s, "UTF-8" ) ],
    cell_filter: Callable[ [ RawCellT ], bool ] = lambda s: True,
    cell_t: Callable[ [ RawCellT ], DataT ] = lambda a: a
) -> Field[ DataT ]:
    height = 0
    width = 0
    cells = [ ]
    for line in lines:
        if line_filter( line ):
            line_cells = line_t( line )
            width = max( width, len( line_cells ) )
            cells.append( [ cell_t( cell ) for cell in line_cells if cell_filter( cell ) ] )
            height += 1
    return Field( width, height, cells )


def field_chars_from_input( lines: Iterable[ str ] ) -> Field[ int ]:
    return field_from_input( lines )


def field_generate[ DataT ]( width: int, height: int, gen_f: Callable[ [ int, int ], DataT ] ) -> Field[ DataT ]:
    return Field( width, height, [ [ gen_f( x, y ) for x in range( width ) ] for y in range( height ) ] )


def field_value[ DataT ]( width: int, height: int, value: DataT ) -> Field[ DataT ]:
    return Field( width, height, [ [ value for cell in range( width ) ] for line in range( height ) ] )


def field_equal_filter[ DataT ]( value: DataT ) -> Callable[ [ int, int, DataT, Field[ DataT ] ], bool ]:
    return lambda _x, _y, v, _f: v == value


def field_digit_cell_t() -> Callable[ [ int ], int ]:
    return lambda v: v - ord( '0' )


def task_check[ DataT, ResultT: str | int ](
    func: Callable[ [ DataT ], ResultT ] | None,
    data: DataT,
    sample: ResultT
):
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
    check_value2: ResultT2 | None
):
    if prepare_fn is not None:
        data = prepare_fn( data )
    task_check( task1_fn, data, check_value1 )
    task_check( task2_fn, data, check_value2 )


def exec_task[ DataT, ResultT: str | int ](
    prepare_fn: Callable[ [ list[ str ] ], DataT ] | None,
    task_fn: Callable[ [ DataT ], ResultT ],
    data: list[ str ] | DataT,
    check_value: ResultT | None
):
    if prepare_fn is not None:
        data = prepare_fn( data )
    task_check( task_fn, data, check_value )


def read_file( file_name: str ) -> list[ str ]:
    with open( file_name ) as file:
        return [ line[ :-1 ] if line[ -1: ] == "\n" else line for line in file.readlines() ]


def print_ex( ex: Exception ):
    [ print( line, file = sys.stderr ) for line in traceback.format_exception( ex ) ]


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


def manhattan( pt1: Coord, pt2: Coord ) -> int:
    return abs( pt1[ 0 ] - pt2[ 0 ] ) + abs( pt1[ 1 ] - pt2[ 1 ] )


def field_rect( width: int, height: int ) -> Rect:
    return 0, 0, width, height
