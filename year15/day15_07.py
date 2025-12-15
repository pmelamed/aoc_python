from enum import Enum

from helper import exec_tasks, print_ex, read_file


class Operation( Enum ):
    NOOP = 0
    NOT = 1
    AND = 2
    OR = 3
    LSHIFT = 4
    RSHIFT = 5


class Source:
    operation: Operation
    src_wire1: str
    src_wire2: str

    def __init__( self, line: str ) -> None:
        sp = line.split( " " )
        if len( sp ) == 1:
            self.operation = Operation.NOOP
            self.src_wire1 = sp[ 0 ]
        elif sp[ 0 ] == "NOT":
            self.operation = Operation.NOT
            self.src_wire1 = sp[ 1 ]
        elif sp[ 1 ] == "AND":
            self.operation = Operation.AND
            self.src_wire1 = sp[ 0 ]
            self.src_wire2 = sp[ 2 ]
        elif sp[ 1 ] == "OR":
            self.operation = Operation.OR
            self.src_wire1 = sp[ 0 ]
            self.src_wire2 = sp[ 2 ]
        elif sp[ 1 ] == "LSHIFT":
            self.operation = Operation.LSHIFT
            self.src_wire1 = sp[ 0 ]
            self.src_wire2 = sp[ 2 ]
        elif sp[ 1 ] == "RSHIFT":
            self.operation = Operation.RSHIFT
            self.src_wire1 = sp[ 0 ]
            self.src_wire2 = sp[ 2 ]


class Data:
    circuit: dict[ str, Source ]

    def __init__( self, lines: list[ str ] ) -> None:
        self.circuit = dict()
        for line in lines:
            sp = line.split( " -> " )
            self.circuit[ sp[ 1 ] ] = Source( sp[ 0 ] )


def task1( data: Data ) -> int:
    return calculate_circuit( "a", data.circuit, dict() )


def task2( data: Data ) -> int:
    a_result = calculate_circuit( "a", data.circuit, dict() )
    return calculate_circuit( "a", data.circuit, { "b": a_result } )


def calculate_circuit( target_wire: str, circuit: dict[ str, Source ], cache: dict[ str, int ] ) -> int:
    if target_wire in cache:
        return cache[ target_wire ]
    if ord( '0' ) <= ord( target_wire[ 0 ] ) <= ord( '9' ):
        value = int( target_wire )
    else:
        gate = circuit[ target_wire ]
        match gate.operation:
            case Operation.NOOP:
                value = calculate_circuit( gate.src_wire1, circuit, cache )
            case Operation.NOT:
                value = ~calculate_circuit( gate.src_wire1, circuit, cache )
            case Operation.AND:
                value = (calculate_circuit( gate.src_wire1, circuit, cache )
                         & calculate_circuit( gate.src_wire2, circuit, cache ))
            case Operation.OR:
                value = (calculate_circuit( gate.src_wire1, circuit, cache )
                         | calculate_circuit( gate.src_wire2, circuit, cache ))
            case Operation.LSHIFT:
                value = (calculate_circuit( gate.src_wire1, circuit, cache )
                         << calculate_circuit( gate.src_wire2, circuit, cache ))
            case Operation.RSHIFT:
                value = (calculate_circuit( gate.src_wire1, circuit, cache )
                         >> calculate_circuit( gate.src_wire2, circuit, cache ))
    cache[ target_wire ] = value
    return value


def main():
    exec_tasks( Data, task1, task2, read_file( '../data/input/year15/day15_07.in' ), 956, 40149 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
