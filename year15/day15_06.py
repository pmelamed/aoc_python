from geom2d import Coord2D, Field2D
from helper import exec_tasks, print_ex, read_file


class Instruction:
    operation: int
    lt: Coord2D
    rb: Coord2D

    def __init__( self, line: str ) -> None:
        sp = line.split( " " )
        if sp[ 0 ] == "turn":
            self.operation = 1 if sp[ 1 ] == "on" else 0
            lt_str = sp[ 2 ]
            rb_str = sp[ 4 ]
        else:
            self.operation = -1
            lt_str = sp[ 1 ]
            rb_str = sp[ 3 ]
        self.lt = Coord2D.from_str( lt_str )
        self.rb = Coord2D.from_str( rb_str )


def parse_data( lines: list[ str ] ) -> list[ Instruction ]:
    return [ Instruction( line ) for line in lines ]


def task1( data: list[ Instruction ] ) -> int:
    display: Field2D[ int ] = Field2D.from_value( 1000, 1000, 0 )
    for instr in data:
        for y in range( instr.lt.y, instr.rb.y + 1 ):
            for x in range( instr.lt.x, instr.rb.x + 1 ):
                match instr.operation:
                    case 0:
                        display.set( x, y, 0 )
                    case 1:
                        display.set( x, y, 1 )
                    case -1:
                        display.set( x, y, 1 - display.get( x, y ) )
    return display.count_if( lambda _x, _y, v: v == 1 )


def task2( data: list[ Instruction ] ) -> int:
    display: Field2D[ int ] = Field2D.from_value( 1000, 1000, 0 )
    for instr in data:
        for y in range( instr.lt.y, instr.rb.y + 1 ):
            for x in range( instr.lt.x, instr.rb.x + 1 ):
                match instr.operation:
                    case 0:
                        display.set( x, y, max( 0, display.get( x, y ) - 1 ) )
                    case 1:
                        display.set( x, y, display.get( x, y ) + 1 )
                    case -1:
                        display.set( x, y, display.get( x, y ) + 2 )
    return sum( display.get( x, y ) for x, y in display.range() )


def main():
    exec_tasks( parse_data, task1, task2, read_file( '../data/input/year15/day15_06.in' ), 400410, 15343601 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
