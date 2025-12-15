from geom2d import Coord2D, SYM_DIRS_2D
from helper import exec_tasks, first_line, print_ex, read_file


def task1( data: str ) -> int:
    current: Coord2D = Coord2D.from_coords( 0, 0 )
    visited: set[ Coord2D ] = { current }
    for direction in data:
        current += SYM_DIRS_2D[ ord( direction ) ]
        visited.add( current )
    return len( visited )


def task2( data: str ) -> int:
    current: list[ Coord2D ] = [
        Coord2D.from_coords( 0, 0 ),
        Coord2D.from_coords( 0, 0 )
    ]
    visited: set[ Coord2D ] = { current[ 0 ] }
    idx = 0
    for direction in data:
        current[ idx ] += SYM_DIRS_2D[ ord( direction ) ]
        visited.add( current[ idx ] )
        idx = 1 - idx
    return len( visited )


def main():
    exec_tasks( first_line, task1, task2, read_file( '../data/input/year15/day15_03.in' ), 2565, 2639 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
