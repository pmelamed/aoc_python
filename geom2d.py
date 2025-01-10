import functools
import itertools
from typing import Callable, Iterable, Optional


@functools.total_ordering
class Coord2D:
    x: int
    y: int

    def __init__( self, x: int, y: int ):
        self.x = x
        self.y = y

    def __add__( self, other ):
        return Coord2D( self.x + other.x, self.y + other.y )

    def __sub__( self, other ):
        return Coord2D( self.x - other.x, self.y - other.y )

    def __str__( self ):
        return f"{self.x},{self.y}"

    def __repr__( self ):
        return f"({self.x},{self.y})"

    def __eq__( self, other ):
        return self.x == other.x and self.y == other.y

    def __lt__( self, other ):
        return self.x < other.x if self.y == other.y else self.y < other.y

    def __hash__( self ):
        return (self.y << 16) ^ self.x

    def manhattan( self ):
        return self.x + self.y

    @classmethod
    def from_coords( cls, x: int, y: int ):
        return cls( x, y )

    @classmethod
    def from_tuple( cls, t: tuple[ int, int ] ):
        return cls( t[ 0 ], t[ 1 ] )

    @classmethod
    def key_x( cls, self ):
        return self.x

    @classmethod
    def key_y( cls, self ):
        return self.y

    @classmethod
    def key_manhattan( cls, self ):
        return self.manhattan()


class Rect2D:
    a: Coord2D
    b: Coord2D

    def __init__( self, a: Coord2D, b: Coord2D ):
        self.a = a
        self.b = b

    def __str__( self ):
        return f"{self.a}~{self.b}"

    def square( self ):
        s = self.a - self.b
        return abs( s.x * s.y )

    @classmethod
    def from_corners( cls, a: Coord2D, b: Coord2D, /, *, sort = False ):
        if sort:
            return Rect2D( Coord2D.from_coords( min( a.x, b.x ), min( a.y, b.y ) ),
                           Coord2D.from_coords( max( a.x, b.x ), max( a.y, b.y ) ) )
        else:
            return Rect2D( Coord2D.from_coords( a.x, a.y ),
                           Coord2D.from_coords( b.x, b.y ) )

    @classmethod
    def from_coords( cls, x1: int, y1: int, x2: int, y2: int, /, *, sort = False ):
        return Rect2D.from_corners( Coord2D.from_coords( x1, y1 ),
                                    Coord2D.from_coords( x2, y2 ),
                                    sort = sort )

    @classmethod
    def from_coords_list( cls, coords: Iterable[ int ], /, *, sort = False ):
        ts = iter( coords )
        return Rect2D.from_corners( Coord2D.from_coords( next( ts ), next( ts ) ),
                                    Coord2D.from_coords( next( ts ), next( ts ) ),
                                    sort = sort )


class Field2D[ DataT ]:
    cells: list[ list[ DataT ] ]
    height: int
    width: int

    def __init__( self, width: int, height: int, cells: list[ list[ DataT ] ] ):
        self.width = width
        self.height = height
        self.cells = cells

    def __getitem__( self, item: Coord2D ) -> DataT:
        return self.cells[ item.y ][ item.x ]

    def __setitem__( self, item: Coord2D, v: DataT ) -> DataT:
        self.cells[ item.y ][ item.x ] = v
        return v

    def __contains__( self, item: Coord2D ):
        return self.contains( item )

    def copy( self ):
        return Field2D( self.width, self.height, [ line.copy() for line in self.cells ] )

    def contains( self, pt: Coord2D ):
        return 0 <= pt.x < self.width and 0 <= pt.y < self.height

    def filter(
        self,
        filter_fn: Callable[ [ int, int, DataT ], bool ]
    ) -> Iterable[ tuple[ int, int, DataT ] ]:
        return Field2DFilterIterator( self, filter_fn )

    def find( self, filter_fn: Callable[ [ int, int, DataT ], bool ] ) -> Optional[ Coord2D ]:
        for y in range( self.height ):
            for x in range( self.width ):
                if filter_fn( x, y, self.cells[ y ][ x ] ): return Coord2D.from_coords( x, y )
        return None

    def update( self, update_fn: Callable[ [ int, int, DataT ], DataT ] ) -> None:
        for y in range( self.height ):
            for x in range( self.width ):
                self.cells[ y ][ x ] = update_fn( x, y, self.cells[ y ][ x ] )

    def dump(
        self, cell_str_f: Callable[ [ int, int, DataT ], str ] = lambda x, y, cell: str( cell ), delim: str = " "
    ) -> str:
        strs = [ [ cell_str_f( x, y, self.cells[ y ][ x ] ) for x in range( self.width ) ]
                 for y in range( self.height ) ]
        cell_width = max( max( len( cell ) for cell in line ) for line in strs )
        return "\n".join( delim.join( cell.rjust( cell_width, " " ) for cell in line ) for line in strs )

    def range( self ) -> Iterable[ tuple[ int, int ] ]:
        return itertools.product( range( self.width ), range( self.height ) )

    @classmethod
    def from_input[ DataT, RawCellT ](
        cls,
        lines: Iterable[ str ],
        /, *,
        line_filter: Callable[ [ str ], bool ] = lambda s: True,
        line_t: Callable[ [ str ], list[ RawCellT ] ] =
        lambda s: [ c for c in bytes( s, "UTF-8" ) ],
        cell_filter: Callable[ [ RawCellT ], bool ] = lambda s: True,
        cell_t: Callable[ [ RawCellT ], DataT ] = lambda a: a
    ):
        height = 0
        width = 0
        cells = [ ]
        for line in lines:
            if line_filter( line ):
                line_cells = line_t( line )
                width = max( width, len( line_cells ) )
                cells.append( [ cell_t( cell ) for cell in line_cells if cell_filter( cell ) ] )
                height += 1
        return cls( width, height, cells )

    @classmethod
    def from_generate[ DataT ]( cls,
                                width: int,
                                height: int,
                                gen_f: Callable[ [ Coord2D ], DataT ] ):
        return cls( width, height, [ [ gen_f( Coord2D( x, y ) ) for x in range( width ) ] for y in range( height ) ] )

    @classmethod
    def from_value[ DataT ]( cls, width: int, height: int, value: DataT ):
        return cls( width, height, [ [ value for _ in range( width ) ] for _ in range( height ) ] )


class Field2DFilterIterator[ DataT ]:
    x: int
    y: int
    field: Field2D[ DataT ]
    filter_fn: Callable[ [ int, int, DataT ], bool ]

    def __init__(
        self,
        field: Field2D[ DataT ],
        filter_fn: Callable[ [ int, int, DataT ], bool ]
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
                if self.filter_fn( self.x, self.y, self.field.cells[ self.y ][ self.x ] ):
                    self.x += 1
                    return self.x - 1, self.y, self.field.cells[ self.y ][ self.x - 1 ]
                self.x += 1
            self.x = 0
            self.y += 1
        raise StopIteration()


def field_equal_filter[ DataT ]( value: DataT ) -> Callable[ [ int, int, DataT ], bool ]:
    return lambda _x, _y, v: v == value


def field_digit_cell_t() -> Callable[ [ int ], int ]:
    return lambda v: v - ord( '0' )


SYM_UP = ord( "^" )
SYM_LEFT = ord( "<" )
SYM_RIGHT = ord( ">" )
SYM_DOWN = ord( "v" )
SYM_DIRS_2D = {
    SYM_RIGHT: Coord2D( 1, 0 ),
    SYM_DOWN:  Coord2D( 0, 1 ),
    SYM_LEFT:  Coord2D( -1, 0 ),
    SYM_UP:    Coord2D( 0, -1 )
}
