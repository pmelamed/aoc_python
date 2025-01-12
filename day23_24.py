from functools import partial

from sympy import nonlinsolve, symbols

from geom2d import Coord2D
from geom3d import Coord3D, Rect3D
from helper import exec_tasks, print_ex, read_file

START_POINT = Coord2D.from_coords( 1, 0 )


class Stone:
    p: Coord3D
    v: Coord3D

    def __init__( self, p: Coord3D, v: Coord3D ):
        self.p = p
        self.v = v

    def __repr__( self ):
        return f"{self.p} @ {self.v}"


class Data:
    stones: list[ Stone ]
    rng: Rect3D

    def __init__( self, lines: list[ str ], rng: Rect3D ):
        self.stones = list( [ parse_stone( line ) for line in lines ] )
        self.rng = rng


def task1( data: Data ) -> int:
    count = 0
    for index1, stone1 in enumerate( data.stones[ :-1 ] ):
        for index2, stone2 in enumerate( data.stones[ index1 + 1: ] ):
            if is_simple_intersect( stone1, stone2, data.rng ):
                count += 1
    return count


def task2( data: Data ) -> int:
    # p1 + t1 * v1 = pr + t1 * vr --> t1 = (pr - p1)/(v1 - vr)
    # t1 * vx1 + px1 = t1 * vxr + pxr --> t1 * vxr - t1 * vx1 + pxr - px1
    s1, s2, s3 = data.stones[ 0:3 ]
    xvars = symbols( "pxr pyr pzr vxr vyr vzr t1 t2 t3" )
    pxr, pyr, pzr, vxr, vyr, vzr, t1, t2, t3 = xvars
    solution = nonlinsolve( [
        t1 * vxr - t1 * s1.v.x + pxr - s1.p.x,
        t1 * vyr - t1 * s1.v.y + pyr - s1.p.y,
        t1 * vzr - t1 * s1.v.z + pzr - s1.p.z,
        t2 * vxr - t2 * s2.v.x + pxr - s2.p.x,
        t2 * vyr - t2 * s2.v.y + pyr - s2.p.y,
        t2 * vzr - t2 * s2.v.z + pzr - s2.p.z,
        t3 * vxr - t3 * s3.v.x + pxr - s3.p.x,
        t3 * vyr - t3 * s3.v.y + pyr - s3.p.y,
        t3 * vzr - t3 * s3.v.z + pzr - s3.p.z
    ], xvars )
    sol = next( iter( solution ) )
    return int( sol[ 0 ] + sol[ 1 ] + sol[ 2 ] )


def parse_stone( line: str ) -> Stone:
    s1 = line.split( " @ " )
    crd = s1[ 0 ].split( ", " )
    vel = s1[ 1 ].split( ", " )
    return Stone( Coord3D( int( crd[ 0 ] ), int( crd[ 1 ] ), int( crd[ 2 ] ) ),
                  Coord3D( int( vel[ 0 ] ), int( vel[ 1 ] ), int( vel[ 2 ] ) ) )


def is_simple_intersect( s1: Stone, s2: Stone, rng: Rect3D ) -> bool:
    d = (s1.v.x * s2.v.y - s2.v.x * s1.v.y)
    if d == 0:
        return False
    t1 = ((s2.p.x - s1.p.x) * s2.v.y + (s1.p.y - s2.p.y) * s2.v.x) / d
    if t1 < 0:
        return False
    t2 = ((s2.p.x - s1.p.x) * s1.v.y + (s1.p.y - s2.p.y) * s1.v.x) / d
    if t2 < 0:
        return False
    xc = s1.p.x + t1 * s1.v.x
    yc = s1.p.y + t1 * s1.v.y
    return rng.a.x <= xc <= rng.b.x and rng.a.y <= yc <= rng.b.y


def main():
    exec_tasks( partial( Data, rng = Rect3D.from_coords( 7, 7, 0, 27, 27, 0 ) ),
                task1,
                task2,
                read_file( 'data/day23_24.sample' ),
                2,
                47 )
    exec_tasks( partial( Data, rng = Rect3D.from_coords( 200000000000000,
                                                         200000000000000,
                                                         0,
                                                         400000000000000,
                                                         400000000000000,
                                                         0 ) ),
                task1,
                task2,
                read_file( 'data/day23_24.in' ),
                28174,
                568386357876600 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
