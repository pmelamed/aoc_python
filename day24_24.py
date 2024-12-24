import itertools
from typing import Callable

from helper import exec_task, exec_tasks, print_ex, read_file

OPERATIONS = {
    "AND": lambda in1, in2: in1 & in2,
    "OR":  lambda in1, in2: in1 | in2,
    "XOR": lambda in1, in2: in1 ^ in2,
    "0":   lambda in1, in2: 0,
    "1":   lambda in1, in2: 1
}

class Gate:
    in1: str
    in2: str
    name: str
    op: Callable[ [ int, int ], int ]

    def __init__( self, in1: str, in2: str, name: str, op: Callable[ [ int, int ], int ] ):
        self.in1 = in1
        self.in2 = in2
        self.name = name
        self.op = op

class GateError:
    gate: Gate
    expected: int


class Data:
    gates: dict[ str, Gate ]
    ordered: list[ Gate ]
    z_gates: list[ str ]

    def __init__( self, lines: list[ str ] ):
        self.gates = dict()
        for line in itertools.takewhile( lambda l: l != "", lines ):
            name, val = line.split( ": " )
            self.gates[ name ] = Gate( "", "", name, OPERATIONS[ val ] )
        for line in itertools.islice( itertools.dropwhile( lambda l: l != "", lines ), 1, None, None ):
            in1, op, in2, _, name = line.split( " " )
            self.gates[ name ] = Gate( in1, in2, name, OPERATIONS[ op ] )
        self.z_gates = sorted( key for key in self.gates.keys() if key[ 0 ] == "z" )
        self.ordered = [ ]
        gates_fifo = list( self.gates[ key ] for key in self.z_gates )
        while gates_fifo:
            gate = gates_fifo.pop( 0 )
            self.ordered.append( gate )
            if gate.in1 != "": gates_fifo.append( self.gates[ gate.in1 ] )
            if gate.in2 != "": gates_fifo.append( self.gates[ gate.in2 ] )
        self.ordered.reverse()


def task1( data: Data ) -> int:
    values: dict[ str, int ] = { "": 0 }
    return process_logic( data, values )



def task2( data: Data ) -> int:
    return 0


def process_logic( data, values ) -> int:
    for gate in data.ordered:
        values[ gate.name ] = gate.op( values[ gate.in1 ], values[ gate.in2 ] )
    return sum( values[ gate ] << int( gate[ 1: ], 10 ) for gate in data.z_gates )


def compare_gates( ga: Gate, gb: Gate ) -> int:
    if gb.in1 == ga.name or gb.in2 == ga.name: return -1
    if ga.in1 == gb.name or ga.in2 == gb.name: return 1
    return (-1 if ga.name < gb.name
            else 1 if ga.name > gb.name else 0)


def main():
    exec_tasks(
        Data,
        task1,
        task2,
        read_file( 'data/day24_24.sample' ),
        2024,
        None
    )
    exec_tasks(
        Data,
        task1,
        task2,
        read_file( 'data/day24_24.in' ),
        56939028423824,
        None
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
