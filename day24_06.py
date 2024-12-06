from collections.abc import Iterable

import helper

VISITED_CELL = ord( 'x' )
OBSTACLE = ord( '#' )
VISITED_OBSTACLE = ord( '*' )


class Data:
    obstacles: set[ tuple[ int, int ] ]
    field: list[ bytearray ]
    start_position: tuple[ int, int ]
    size: tuple[ int, int ]

    def __init__( self,
                  field: list[ bytearray ],
                  obstacles: set[ tuple[ int, int ] ],
                  start_position: tuple[ int, int ] ):
        self.size = (len( field[ 0 ] ), len( field ))
        self.field = field
        self.obstacles = obstacles
        self.start_position = start_position

    def copy_field( self ):
        return [ line.copy() for line in self.field ]


def prepare( lines: Iterable[ str ] ) -> Data:
    pos = None
    obstacles = set()
    field = [ bytearray( line, "UTF-8" ) for line in lines ]
    y = 0
    for line in lines:
        x = 0
        for cell in line:
            match cell:
                case "^":
                    pos = (x, y)
                case "#":
                    obstacles.add( (x, y) )
            x += 1
        y += 1
    return Data( field, obstacles, pos )


def task1( data: Data ) -> int:
    pos = data.start_position
    direction = (0, -1)
    field = data.copy_field()
    while 0 <= pos[ 0 ] < data.size[ 0 ] and 0 <= pos[ 1 ] < data.size[ 1 ]:
        if field[ pos[ 1 ] ][ pos[ 0 ] ] == OBSTACLE:
            pos = (pos[ 0 ] - direction[ 0 ], pos[ 1 ] - direction[ 1 ])
            direction = helper.turn_right( direction )
        else:
            field[ pos[ 1 ] ][ pos[ 0 ] ] = VISITED_CELL
        pos = (pos[ 0 ] + direction[ 0 ], pos[ 1 ] + direction[ 1 ])
    return sum( [ helper.count_if( lambda c: c == VISITED_CELL, line ) for line in field ] )


def task2( data: Data ) -> int:
    pos = data.start_position
    direction = (0, -1)
    field = data.copy_field()
    added_obstacles = 0
    while 0 <= pos[ 0 ] < data.size[ 0 ] and 0 <= pos[ 1 ] < data.size[ 1 ]:
        if field[ pos[ 1 ] ][ pos[ 0 ] ] == OBSTACLE:
            field[ pos[ 1 ] ][ pos[ 0 ] ] = VISITED_OBSTACLE
            pos = (pos[ 0 ] - direction[ 0 ], pos[ 1 ] - direction[ 1 ])
            direction = helper.turn_right( direction )
        else:
            field[ pos[ 1 ] ][ pos[ 0 ] ] = VISITED_CELL
            added_obstacles += should_place_cell( pos, direction, data.size, field )
        pos = (pos[ 0 ] + direction[ 0 ], pos[ 1 ] + direction[ 1 ])
    return added_obstacles


def should_place_cell( pos: tuple[ int, int ],
                       direction: tuple[ int, int ],
                       size: tuple[ int, int ],
                       field: list[ bytearray ] ) -> int:
    x = pos[ 0 ] + direction[ 0 ]
    y = pos[ 1 ] + direction[ 1 ]
    if x < 0 or x >= size[ 0 ] or y < 0 or y > size[ 1 ] or field[ y ][ x ] == OBSTACLE: return 0
    d = helper.turn_right( direction )
    x = pos[ 0 ]
    y = pos[ 1 ]
    while 0 <= x < size[ 0 ] and 0 <= y < size[ 1 ] and field[ y ][ x ] != OBSTACLE:
        if field[ y ][ x ] == VISITED_OBSTACLE:
            print( (pos[ 0 ] + direction[ 0 ], pos[ 1 ] + direction[ 1 ]) )
            return 1
        x += d[ 0 ]
        y += d[ 1 ]
    return 0


def main():
    helper.exec_tasks( prepare, task1, task2, helper.read_file( 'data/day24_06.sample' ), 41, 6 )
    helper.exec_tasks( prepare, task1, task2, helper.read_file( 'data/day24_06.in' ), 5564, None )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        helper.print_ex( ex )
