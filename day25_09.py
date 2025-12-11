import itertools
from bisect import bisect_left
from typing import Iterable

from PIL import Image, ImageDraw

from geom2d import CROSS_DIRS_2D, Coord2D, Field2D
from helper import exec_tasks, print_ex, read_file


class Square:
    tile1_idx: int
    tile1: Coord2D
    tile2_idx: int
    tile2: Coord2D
    square: int

    def __init__( self, tile1_idx: int, tile1: Coord2D, tile2_idx: int, tile2: Coord2D ):
        self.tile1_idx = tile1_idx
        self.tile1 = tile1
        self.tile2_idx = tile2_idx
        self.tile2 = tile2
        diff = tile2 - tile1
        self.square = (abs( diff.x ) + 1) * (abs( diff.y ) + 1)


class Data:
    tiles: list[ Coord2D ]
    sorted_squares: list[ Square ]

    def __init__( self, lines: list[ str ] ):
        self.tiles = [ Coord2D.from_str( line ) for line in lines ]
        self.sorted_squares = [ ]
        for idx1 in range( len( self.tiles ) - 1 ):
            for idx2 in range( idx1 + 1, len( self.tiles ) ):
                self.sorted_squares.append( Square( idx1, self.tiles[ idx1 ], idx2, self.tiles[ idx2 ] ) )
        self.sorted_squares.sort( key = lambda sq: sq.square, reverse = True )


def task1( data: Data ) -> int:
    return data.sorted_squares[ 0 ].square
    # result = 0
    # for idx1 in range( len( data.tiles ) - 1 ):
    #     for idx2 in range( idx1 + 1, len( data.tiles ) ):
    #         tile1 = data.tiles[ idx1 ]
    #         tile2 = data.tiles[ idx2 ]
    #         diff = tile2 - tile1
    #         square = (abs( diff.x ) + 1) * (abs( diff.y ) + 1)
    #         if square > result:
    #             result = square
    # return result


def task2( data: Data ) -> int:
    x_cells = make_sparce_axis( tile.x for tile in data.tiles )
    y_cells = make_sparce_axis( tile.y for tile in data.tiles )

    width = len( x_cells )
    height = len( y_cells )

    compressed_tiles: list[ Coord2D ] = [
        compress_tile( tile, [ x[ 0 ] for x in x_cells ], [ y[ 0 ] for y in y_cells ] ) for tile in data.tiles
    ]
    # print( f"{data.tiles}" )
    # print( f"{width} -> {x_cells} -> {compressed_tiles}" )
    bitmap: Field2D[ int ] = Field2D.from_value( width, height, 0 )
    for idx in range( len( compressed_tiles ) ):
        tile1 = compressed_tiles[ idx ]
        tile2 = compressed_tiles[ (idx + 1) % len( compressed_tiles ) ]
        if tile1.x == tile2.x:
            for y in range( min( tile1.y, tile2.y ), max( tile1.y, tile2.y ) + 1 ):
                bitmap.set( tile1.x, y, 1 )
        else:
            for x in range( min( tile1.x, tile2.x ), max( tile1.x, tile2.x ) + 1 ):
                bitmap.set( x, tile1.y, 1 )
    wave: list[ Coord2D ] = [ Coord2D.from_coords( 0, 0 ) ]
    while len( wave ) > 0:
        cell = wave.pop()
        bitmap[ cell ] = 2
        for new_cell in [ cell + delta for delta in CROSS_DIRS_2D ]:
            if bitmap.contains( new_cell ) and bitmap[ new_cell ] == 0:
                wave.append( new_cell )
    for square in data.sorted_squares:
        if check_square( compressed_tiles[ square.tile1_idx ], compressed_tiles[ square.tile2_idx ], bitmap ):
            return square.square
    return 0


def check_square( corner1: Coord2D, corner2: Coord2D, bitmap: Field2D[ int ] ):
    return all(
            bitmap.get( xc, yc ) != 2 for xc, yc in itertools.product(
                    range( min( corner1.x, corner2.x ), max( corner1.x, corner2.x ) + 1 ),
                    range( min( corner1.y, corner2.y ), max( corner1.y, corner2.y ) + 1 )
            )
    )


def make_sparce_axis( in_coords: Iterable[ int ] ) -> list[ tuple[ int, int ] ]:
    coords = list( set( in_coords ) )
    coords.sort()
    lo: list[ int ] = [ ]
    hi: list[ int ] = [ ]
    lo.append( coords[ 0 ] - 1 )
    hi.append( coords[ 0 ] - 1 )
    for index in range( len( coords ) - 1 ):
        lo.append( coords[ index ] )
        hi.append( coords[ index ] )
        if coords[ index + 1 ] - coords[ index ] > 1:
            lo.append( coords[ index ] + 1 )
            hi.append( coords[ index + 1 ] - 1 )
    lo.append( coords[ -1 ] )
    hi.append( coords[ -1 ] )
    lo.append( coords[ -1 ] + 1 )
    hi.append( coords[ -1 ] + 1 )
    return list( zip( lo, hi ) )


def compress_tile( tile: Coord2D, x: list[ int ], y: list[ int ] ):
    return Coord2D.from_coords( bisect_left( x, tile.x ), bisect_left( y, tile.y ) )


def main():
    exec_tasks( Data, task1, task2, read_file( 'data/day25_09.sample' ), 50, 24 )
    exec_tasks( Data, task1, task2, read_file( 'data/day25_09.in' ), 4749672288, 1479665889 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
