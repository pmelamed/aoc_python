from collections import defaultdict

from geom2d import Field2D
from helper import exec_tasks, print_ex, read_file


class Data:
    splitters: Field2D[ bool ]
    start_x: int

    def __init__( self, lines: list[ str ] ):
        self.splitters = Field2D.from_input(
                lines,
                cell_t = lambda c: c == ord( "^" )
        )
        self.start_x = lines[ 0 ].index( "S" )


def task1( data: Data ) -> int:
    result: int = 0
    beams: set[ int ] = { data.start_x }
    for y in range( 1, data.splitters.height ):
        next_beams = set()
        for beam in beams:
            if data.splitters.get( beam, y ):
                result += 1
                next_beams.add( beam - 1 )
                next_beams.add( beam + 1 )
            else:
                next_beams.add( beam )
        beams = next_beams
    return result


def task2( data: Data ) -> int:
    result: int = 0
    beams: dict[ int, int ] = defaultdict( lambda: 0, { data.start_x: 1 } )
    for y in range( 1, data.splitters.height ):
        next_beams = defaultdict( lambda: 0 )
        for x, count in beams.items():
            if data.splitters.get( x, y ):
                next_beams[ x - 1 ] += count
                next_beams[ x + 1 ] += count
            else:
                next_beams[ x ] += count
        beams = next_beams
    return sum( beams.values() )


def main():
    exec_tasks( Data, task1, task2, read_file( 'data/day25_07.sample' ), 21, 40 )
    exec_tasks( Data, task1, task2, read_file( 'data/day25_07.in' ), 1615, 43560947406326 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
