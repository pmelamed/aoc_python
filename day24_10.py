from collections import defaultdict

import helper
from helper import Coord, Field, field_equal_filter, CROSS_DIRS, exec_tasks, move_forward, read_file, print_ex


class Data:
    field: Field[ int ]

    def __init__( self,
                  field: Field[ int ] ):
        self.field = field


def prepare( lines: list[ str ] ) -> Data:
    return Data( helper.field_from_input( lines, cell_t=lambda c: c - ord( '0' ) ) )


def task1( data: Data ) -> int:
    return sum( (track_trails( data, (x, y) )
                 for x, y, _ in data.field.filter( field_equal_filter( 0 ) )) )


def task2( data: Data ) -> int:
    return sum( (track_distinct_trails( data, (x, y) )
                 for x, y, _ in data.field.filter( field_equal_filter( 0 ) )) )


def track_trails( data: Data, pt: Coord ) -> int:
    wave: set[ Coord ] = set()
    wave.add( pt )
    for level in range( 1, 10 ):
        wave_next: set[ Coord ] = set()
        for wave_pt in wave:
            for dr in CROSS_DIRS:
                pt_next = move_forward( wave_pt, dr )
                if data.field.contains( pt_next ) and data.field[ pt_next ] == level:
                    wave_next.add( pt_next )
        wave = wave_next
    return len( wave )


def track_distinct_trails( data: Data, pt: Coord ) -> int:
    wave: dict[ Coord, int ] = defaultdict( lambda: 0 )
    wave[ pt ] = 1
    for level in range( 1, 10 ):
        wave_next: dict[ Coord, int ] = defaultdict( lambda: 0 )
        for wave_pt in wave.keys():
            trails_count = wave[ wave_pt ]
            for dr in CROSS_DIRS:
                pt_next = move_forward( wave_pt, dr )
                if data.field.contains( pt_next ) and data.field[ pt_next ] == level:
                    wave_next[ pt_next ] += trails_count
        wave = wave_next
    return sum( wave.values() )


def main():
    exec_tasks( prepare, task1, task2, read_file( 'data/day24_10.sample' ), 36, 81 )
    exec_tasks( prepare, task1, task2, read_file( 'data/day24_10.in' ), 682, 1511 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
