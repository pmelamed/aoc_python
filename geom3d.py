from typing import Iterable


class Coord3D:
    x: int
    y: int
    z: int

    def __init__( self, x: int, y: int, z: int ):
        self.x = x
        self.y = y
        self.z = z

    def __add__( self, other ):
        return Coord3D( self.x + other.x, self.y + other.y, self.z + other.z )

    def __sub__( self, other ):
        return Coord3D( self.x - other.x, self.y - other.y, self.z - other.z )

    def __str__( self ):
        return f"{self.x},{self.y},{self.z}"

    def manhattan( self ):
        return self.x + self.y + self.z

    @classmethod
    def from_coords( cls, x: int, y: int, z: int ):
        return cls( x, y, z )

    @classmethod
    def from_tuple( cls, t: tuple[ int, int, int ] ):
        return cls( t[ 0 ], t[ 1 ], t[ 2 ] )

    @classmethod
    def key_x( cls, self ):
        return self.x

    @classmethod
    def key_y( cls, self ):
        return self.y

    @classmethod
    def key_z( cls, self ):
        return self.z

    @classmethod
    def key_manhattan( cls, self ):
        return self.manhattan()


class Rect3D:
    a: Coord3D
    b: Coord3D

    def __init__( self, a: Coord3D, b: Coord3D ):
        self.a = a
        self.b = b

    def __str__( self ):
        return f"{self.a}~{self.b}"

    def volume( self ):
        s = self.a - self.b
        return abs( s.x * s.y * s.z )

    @classmethod
    def from_corners( cls, a: Coord3D, b: Coord3D, /, *, sort = False ):
        if sort:
            return Rect3D( Coord3D.from_coords( min( a.x, b.x ), min( a.y, b.y ), min( a.z, b.z ) ),
                           Coord3D.from_coords( max( a.x, b.x ), max( a.y, b.y ), max( a.z, b.z ) ) )
        else:
            return Rect3D( Coord3D.from_coords( a.x, a.y, a.z ),
                           Coord3D.from_coords( b.x, b.y, b.z ) )

    @classmethod
    def from_coords( cls, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int, /, *, sort = False ):
        return Rect3D.from_corners( Coord3D.from_coords( x1, y1, z1 ),
                                    Coord3D.from_coords( x2, y2, z2 ),
                                    sort = sort )

    @classmethod
    def from_coords_list( cls, coords: Iterable[ int ], /, *, sort = False ):
        ts = iter( coords )
        return Rect3D.from_corners( Coord3D.from_coords( next( ts ), next( ts ), next( ts ) ),
                                    Coord3D.from_coords( next( ts ), next( ts ), next( ts ) ),
                                    sort = sort )
