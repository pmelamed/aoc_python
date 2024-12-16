from typing import Optional

from helper import print_ex, Coord, exec_tasks, Field, field_from_input, move_forward, Direction, field_value, \
    turn_cw90, read_file, turn_ccw90, CROSS_DIRS


class WaveCell:
    coord: Coord
    direction: Direction
    points: int
    parent: Optional[ object ]

    def __init__( self,
                  coord: Coord,
                  direction: Direction,
                  points: int,
                  parent: Optional[ object ] ):
        self.coord = coord
        self.direction = direction
        self.points = points
        self.parent = parent


class Data:
    field: Field[ int ]
    start: Coord
    end: Coord
    min_ways: list[ WaveCell ]

    def __init__( self,
                  field: Field[ int ],
                  start: Coord,
                  end: Coord ):
        self.field = field
        self.start = start
        self.end = end
        self.min_ways = [ ]


OBSTACLE = ord( '#' )
START = ord( 'S' )
END = ord( 'E' )
EMPTY = ord( '.' )

DIR_CHARS = {
    (-1, 0): ord( '<' ),
    (1, 0): ord( '>' ),
    (0, -1): ord( '^' ),
    (0, 1): ord( 'v' )
}


def prepare( lines: list[ str ] ) -> Data:
    field = field_from_input( lines )
    start = field.find( lambda _x, _y, v, _f: v == START )
    end = field.find( lambda _x, _y, v, _f: v == END )
    return Data( field, start, end )


def task1( data: Data ) -> int:
    way_fields = dict( [ (d, field_value( data.field.width, data.field.height, -1 )) for d in CROSS_DIRS ] )
    wave: list[ WaveCell ] = [ WaveCell( data.start, (1, 0), 0, None ) ]
    min_points = -1
    while wave:
        front = wave.pop()
        if not is_lower_equal( front.points, min_points ): continue
        if data.field[ front.coord ] == OBSTACLE: continue
        if data.field[ front.coord ] == END:
            if front.points < min_points: data.min_ways.clear()
            min_points = front.points
            data.min_ways.append( front )
            continue
        way_field = way_fields[ front.direction ]
        if is_lower_equal( front.points, way_field[ front.coord ] ):
            way_field[ front.coord ] = front.points
            if front.coord != data.end:
                wave.append( WaveCell( move_forward( front.coord, front.direction ),
                                       front.direction,
                                       front.points + 1,
                                       front ) )
                direction = turn_cw90( front.direction )
                wave.append( WaveCell( move_forward( front.coord, direction ),
                                       direction,
                                       front.points + 1001,
                                       front ) )
                direction = turn_ccw90( front.direction )
                wave.append( WaveCell( move_forward( front.coord, direction ),
                                       direction,
                                       front.points + 1001,
                                       front ) )
    return min_points


def task2( data: Data ) -> int:
    seats = set()
    for tail in data.min_ways:
        cell = tail
        while cell is not None:
            seats.add( cell.coord )
            cell = cell.parent
    return len( seats )


def is_lower_equal( way_pts: int, field_pts: int ) -> bool:
    return field_pts == -1 or way_pts <= field_pts


def main():
    exec_tasks( prepare, task1, task2, read_file( 'data/day24_16_1.sample' ), 7036, 45 )
    exec_tasks( prepare, task1, task2, read_file( 'data/day24_16_2.sample' ), 11048, 64 )
    exec_tasks( prepare, task1, task2, read_file( 'data/day24_16.in' ), 134588, 631 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
