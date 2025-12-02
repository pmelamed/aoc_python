import itertools
from typing import Optional

from helper import exec_task, exec_tasks, print_ex, read_file


OPERATIONS = {
    "AND": lambda in1, in2: in1 & in2,
    "OR" : lambda in1, in2: in1 | in2,
    "XOR": lambda in1, in2: in1 ^ in2
}


class Gate:
    ins: set[ str ]
    name: str
    op_name: str

    def __init__(
            self,
            in1: str,
            in2: str,
            name: str,
            op_name: str
            ):
        self.ins = { in1, in2 }
        self.name = name
        self.op_name = op_name


class GateSources:
    local_sum: Gate
    carry_or: Gate


class Data:
    gates: dict[ str, Gate ]
    init_values: dict[ str, int ]
    ordered: list[ Gate ]
    z_gates: list[ str ]

    def __init__( self, lines: list[ str ] ):
        self.init_values = dict()
        for line in itertools.takewhile( lambda l: l != "", lines ):
            name, val = line.split( ": " )
            self.init_values[ name ] = int( val )
        self.gates = dict()
        for line in lines[ len( self.init_values ) + 1: ]:
            in1, op, in2, _, name = line.split( " " )
            self.gates[ name ] = Gate( in1, in2, name, op )
        self.z_gates = sorted( key for key in self.gates.keys() if key[ 0 ] == "z" )
        self.ordered = [ ]
        gates_fifo = list( self.gates[ key ] for key in self.z_gates )
        while gates_fifo:
            gate = gates_fifo.pop( 0 )
            self.ordered.append( gate )
            for input_pin in gate.ins:
                if input_pin[ 0 ] != "x" and input_pin[ 0 ] != "y":
                    gates_fifo.append( self.gates[ input_pin ] )
        self.ordered.reverse()


def task1( data: Data ) -> int:
    values: dict[ str, int ] = data.init_values.copy()
    for gate in data.ordered:
        if gate.name not in values:
            values[ gate.name ] = OPERATIONS[ gate.op_name ]( *[ values[ input_pin ] for input_pin in gate.ins ] )
    return sum( values[ gate1 ] << int( gate1[ 1: ], 10 ) for gate1 in data.z_gates )


def task2( data: Data ) -> str:
    not_found: set[ str ] = set()
    local_sum = find_gate( data.gates, "XOR", "x01", "y01", not_found )
    carry_or = find_gate( data.gates, "AND", "x00", "y00", not_found )
    find_gate( data.gates, "AND", carry_or.name, local_sum.name, not_found )
    for index in range( 2, len( data.z_gates ) - 1 ):
        local_sum, carry_or = fill_section( local_sum, carry_or, data.gates, index, not_found )
    return ",".join( sorted( not_found ) )


def fill_section(
        local_sum: Gate,
        carry_or: Gate,
        gates: dict[ str, Gate ],
        index: int,
        not_found: set[ str ]
        ) -> tuple[ Gate, Gate ]:
    result_local_sum = find_gate(
        gates,
        "XOR",
        gate_name( "x", index ),
        gate_name( "y", index ),
        not_found
        )
    carry_and_direct = find_gate(
        gates,
        "AND",
        gate_name( "x", index - 1 ),
        gate_name( "y", index - 1 ),
        not_found
        )
    carry_and_indirect = find_gate(
        gates,
        "AND",
        local_sum.name,
        carry_or.name,
        not_found
        )
    result_carry_or = find_gate(
        gates,
        "OR",
        carry_and_direct.name,
        carry_and_indirect.name,
        not_found
        )
    find_gate( gates, "XOR", result_local_sum.name, result_carry_or.name, not_found )
    return result_local_sum, result_carry_or


def find_gate( gates: dict[ str, Gate ], op_name: str, in1: str, in2: str, not_found: set[ str ] ) -> Gate:
    zipped = ((match_gate( gate, op_name, in1, in2 ), gate) for gate in gates.values())
    pairs = sorted(
            ((mismatch, gate) for mismatch, gate in zipped if mismatch is not None and len( mismatch ) < 4),
            key = lambda pair: len( pair[ 0 ] )
            )
    if not pairs:
        raise RuntimeError( f"Gate not found {op_name}( {in1}, {in2} )" )
    mismatch, gate = pairs[ 0 ]
    not_found.update( mismatch )
    return gate


def match_gate( gate: Gate, op_name: str, in1: str, in2: str ) -> Optional[ set[ str ] ]:
    return gate.ins.symmetric_difference( { in1, in2 } ) if gate.op_name == op_name else None


def gate_name( prefix: str, index: int ):
    return f"{prefix}{index:02d}"


def main():
    exec_task(
            Data,
            task1,
            read_file( 'data/day24_24.sample' ),
            2024
    )
    exec_tasks(
            Data,
            task1,
            task2,
            read_file( 'data/day24_24.in' ),
            56939028423824,
            "frn,gmq,vtj,wnf,wtt,z05,z21,z39"
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
