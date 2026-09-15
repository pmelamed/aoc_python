from numpy import bool

import helper
from geom3d import Coord3D, Rect3D
from helper import create_nd_array, print_ex, read_file


BoolField3D = list[ list[ list[ bool ] ] ]

NEIGHBOURS_X = [
    Coord3D.from_coords( 1, 0, 0 ),
    Coord3D.from_coords( -1, 0, 0 ),
    Coord3D.from_coords( 0, 1, 0 ),
    Coord3D.from_coords( 0, -1, 0 ),
    Coord3D.from_coords( 0, 0, -1 ),
    Coord3D.from_coords( 0, 0, 1 )
]


class Data:
    field: BoolField3D
    points: list[ Coord3D ]
    dims: tuple[ int, int, int ]
    brf_corner: Coord3D
    field_rect: Rect3D

    def __init__(
            self, dims: tuple[ int, int, int ], field: list[ list[ list[ bool ] ] ], points: list[ Coord3D ]
    ) -> None:
        self.dims = dims
        self.field = field
        self.points = points
        self.brf_corner = Coord3D.from_tuple( dims )
        self.field_rect = Rect3D.from_corners( Coord3D.from_coords( 0, 0, 0 ), self.brf_corner )


def parse_data( lines: list[ str ] ) -> Data:
    min_x: int = 100
    min_y: int = 100
    min_z: int = 100
    max_x: int = 0
    max_y: int = 0
    max_z: int = 0
    points: list[ Coord3D ] = [ Coord3D.from_tuple( (int( p[ 0 ] ), int( p[ 1 ] ), int( p[ 2 ] )) )
                                for p in [ l.split( "," ) for l in lines ] ]
    for pt in points:
        min_x = min( min_x, pt.x )
        max_x = max( max_x, pt.x )
        min_y = min( min_y, pt.y )
        max_y = max( max_y, pt.y )
        min_z = min( min_z, pt.z )
        max_z = max( max_z, pt.z )
    dims = (max_x - min_x + 3, max_y - min_y + 3, max_z - min_z + 3)
    field = create_nd_array( dims, value = False )
    adjusted_points = [ Coord3D.from_coords( pt.x - min_x + 1, pt.y - min_y + 1, pt.z - min_z + 1 ) for pt in points ]
    for pt in adjusted_points:
        field[ pt.x ][ pt.y ][ pt.z ] = True
    return Data( dims, field, adjusted_points )


def pack_coords( x: int, y: int, z: int ) -> int:
    print( f"{x},{y},{z}" )
    return ((z << 8) + y) << 8 + x


def task1( data: Data ) -> int:
    return sum( count_free_edges( pt, data ) for pt in data.points )


def task2( data: Data ) -> int:
    result = 0
    outer_points = create_nd_array( data.dims, value = False )
    wave = [ Coord3D.from_coords( 0, 0, 0 ) ]
    while wave:
        pt = wave.pop( 0 )
        if outer_points[ pt.x ][ pt.y ][ pt.z ] :
            continue
        outer_points[ pt.x ][ pt.y ][ pt.z ] = True
        valid_neighbours = [ p for p in get_neighbours( pt ) if p in data.field_rect ]
        result += sum( 1 for p in valid_neighbours if data.field[ p.x ][ p.y ][ p.z ] )
        wave.extend(
                p for p in valid_neighbours
                if not outer_points[ p.x ][ p.y ][ p.z ] and not data.field[ p.x ][ p.y ][ p.z ]
        )
    return result


def count_free_edges( pt: Coord3D, data: Data ) -> int:
    return sum( 1 for n in NEIGHBOURS_X if not data.field[ pt.x + n.x ][ pt.y + n.y ][ pt.z + n.z ] )


def get_neighbours( pt: Coord3D ) -> list[ Coord3D ]:
    return [ Coord3D.from_coords( pt.x + n.x, pt.y + n.y, pt.z + n.z ) for n in NEIGHBOURS_X ]


def main():
    helper.verbose_level = 0
    # helper.exec_tasks(
    #         parse_data,
    #         task1,
    #         task2,
    #         [ "1,1,1", "2,1,1" ],
    #         10,
    #         10
    # )
    # helper.exec_tasks(
    #         parse_data,
    #         task1,
    #         task2,
    #         read_file( '../data/samples/year22/day22_18.sample' ),
    #         64,
    #         58
    # )
    helper.exec_tasks(
            parse_data,
            task1,
            task2,
            read_file( '../data/input/year22/day22_18.in' ),
            4364,
            2508
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
