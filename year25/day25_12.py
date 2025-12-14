from typing import Callable, Literal

from geom2d import Field2D, field_equal_filter
from helper import exec_task, print_ex, read_file


BIT_FN: Callable[ [ int, int, bool ], Literal[ 0, 1 ] ] = lambda _x, _y, v: 1 if v else 0
PATTERN_HEIGHT = 3
PATTERN_WIDTH = 3


class Shape:
    pattern: Field2D[ bool ]
    masks: list[ tuple[ int, ... ] ]
    used_cells: int

    def __init__( self, lines: list[ str ] ):
        self.pattern = Field2D.from_input( lines[ 1:4 ], cell_t = lambda c: c == ord( '#' ) )
        self.masks = (self.make_turned_masks( self.pattern ) +
                      self.make_turned_masks( self.pattern.flip_vertically() ) +
                      self.make_turned_masks( self.pattern.flip_horizontally() ))
        masks_set = set( compact_mask( mask ) for mask in self.masks )
        self.masks = [ decompact_mask( compacted ) for compacted in masks_set ]
        self.used_cells = self.pattern.count_if( field_equal_filter( True ) )

    @staticmethod
    def make_turned_masks( pattern: Field2D[ bool ] ) -> list[ tuple[ int, ... ] ]:
        result = [ ]
        for _ in range( 4 ):
            result.append( tuple( pattern.make_mask( BIT_FN ) ) )
            pattern = pattern.turn90_cw()
        return result


class Area:
    width: int
    height: int
    presents: list[ int ]

    def __init__( self, line: str ):
        split1 = line.split( ": " )
        self.width, self.height = (int( s ) for s in split1[ 0 ].split( "x" ))
        self.presents = [ int( s ) for s in split1[ 1 ].split( " " ) ]


class Data:
    shapes: list[ Shape ]
    areas: list[ Area ]

    def __init__( self, lines: list[ str ] ):
        self.shapes = [ Shape( lines[ shape_idx * 5: shape_idx * 5 + 4 ] ) for shape_idx in range( 6 ) ]
        self.areas = [ Area( line ) for line in lines[ 30: ] ]
        pass


def task1( data: Data ) -> int:
    result = 0
    for area in data.areas:
        used_cells = sum( data.shapes[ i ].used_cells * area.presents[ i ] for i in range( len( data.shapes ) ) )
        if used_cells > area.width * area.height:
            continue
        if area.width // 3 * area.height // 3 > sum( area.presents ):
            result += 1
            continue
        if try_fit_area( area, data.shapes ):
            result += 1
    return result


def try_fit_area( area: Area, shapes: list[ Shape ] ) -> bool:
    all_presents = [ ]
    for shape_idx in range( len( shapes ) ):
        all_presents += area.presents[ shape_idx ] * [ shapes[ shape_idx ] ]
    return try_fit_rest( area, area.height * [ 0 ], all_presents, 0 )


def try_fit_rest( area: Area, mask: list[ int ], presents: list[ Shape ], start_idx: int ) -> bool:
    if start_idx == len( presents ):
        return True
    for present_mask in presents[ start_idx ].masks:
        for x in range( 0, area.width - PATTERN_WIDTH + 1 ):
            pattern = tuple( m << x for m in present_mask )
            for y in range( 0, area.height - PATTERN_HEIGHT + 1 ):
                if not pattern_applicable( y, mask, pattern ):
                    continue
                for apply_y in range( PATTERN_HEIGHT ):
                    mask[ y + apply_y ] ^= pattern[ apply_y ]
                if try_fit_rest( area, mask, presents, start_idx + 1 ):
                    return True
                for apply_y in range( PATTERN_HEIGHT ):
                    mask[ y + apply_y ] ^= pattern[ apply_y ]
    return False


def pattern_applicable( apply_y: int, mask: list[ int ], pattern: tuple[ int, ... ] ) -> bool:
    for y in range( PATTERN_HEIGHT ):
        if mask[ y + apply_y ] & ~pattern[ y ] != mask[ y + apply_y ]:
            return False
    return True


def compact_mask( mask: tuple[ int, ... ] ) -> int:
    return mask[ 0 ] | (mask[ 1 ] << PATTERN_WIDTH) | (mask[ 2 ] << PATTERN_WIDTH * 2)


def decompact_mask( compacted: int ) -> tuple[ int, ... ]:
    return compacted & 7, (compacted >> PATTERN_WIDTH) & 7, (compacted >> PATTERN_WIDTH * 2) & 7


def main():
    exec_task( Data, task1, read_file( '../data/input/year25/day25_12.in' ), 519 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
