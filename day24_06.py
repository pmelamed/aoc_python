import collections
from collections.abc import Callable, Iterable

import helper


class Data:
    obstacles: set[ tuple[ int, int ] ]
    field: list[ bytearray ]
    start_position: tuple[ int, int ]
    rect: tuple[ int, int, int, int ]

    def __init__( self,
                  field: list[ bytearray ],
                  obstacles: set[ tuple[ int, int ] ],
                  start_position: tuple[ int, int ] ):
        self.rect = (0, 0, len( field[ 0 ] ), len( field ))
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
    visited: set[ tuple[ int, int ] ] = set()

    def predicate( pt: tuple[ int, int ], _: tuple[ int, int ] ) -> bool | None:
        visited.add( pt )
        return None

    trace_until( data.start_position, (0, -1), data.obstacles, data.rect, predicate )
    return len( visited )


def task2( data: Data ) -> int:
    added_obstacles: set[ tuple[ int, int ] ] = set()

    for x in range( data.rect[ 2 ] ):
        for y in range( data.rect[ 3 ] ):
            xy = (x, y)
            if data.start_position != xy and not xy in data.obstacles and should_place_obstacle( data, xy ):
                added_obstacles.add( xy )
    return len( added_obstacles )


def should_place_obstacle( data: Data, pos: tuple[ int, int ] ) -> tuple[ int, int ] | None:
    visited: dict[ tuple[ int, int ], set[ tuple[ int, int ] ] ] = collections.defaultdict( set )

    def predicate( pt: tuple[ int, int ], direct: tuple[ int, int ] ) -> bool | None:
        pt_visited = visited[ pt ]
        if direct in pt_visited: return True
        pt_visited.add( direct )
        return None

    data.obstacles.add( pos )
    result = trace_until( data.start_position, (0, -1), data.obstacles, data.rect, predicate )
    data.obstacles.remove( pos )
    return pos if result else None


def trace_until( pos: tuple[ int, int ],
                 direction: tuple[ int, int ],
                 obstacles: set[ tuple[ int, int ] ],
                 rect: tuple[ int, int, int, int ],
                 predicate: Callable[ [ tuple[ int, int ], tuple[ int, int ] ], bool | None ] ) -> bool:
    while helper.inside_rect( pos, rect ):
        if pos in obstacles:
            pos = helper.move_backward( pos, direction )
            direction = helper.turn_cw90( direction )
        else:
            match predicate( pos, direction ):
                case True:
                    return True
                case False:
                    return False
        pos = helper.move_forward( pos, direction )
    return False


def main():
    helper.exec_tasks( prepare, task1, task2, helper.read_file( 'data/day24_06.sample' ), 41, 6 )
    helper.exec_tasks( prepare, task1, task2, helper.read_file( 'data/day24_06.in' ), 5564, 1976 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        helper.print_ex( ex )
