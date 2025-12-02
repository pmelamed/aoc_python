import functools
import math
import re
from collections import defaultdict, deque
from functools import reduce
from typing import Any, Callable, Optional

import helper


class Module:
    type: str
    name: str
    inputs: list[ str ]
    outputs: dict[ str, int ]

    def __init__( self ):
        self.inputs = [ ]
        self.outputs = dict()
        self.type = ""

    def __str__( self ):
        return f"{self.type}/{self.name} {self.inputs} -> {self.outputs}" \
            if hasattr( self, "name" ) \
            else f"N/I ({self.inputs})"


type Modules = dict[ str, Module ]


class SimData:
    ff_states: dict[ str, bool ]
    inv_inputs: dict[ str, list[ bool ] ]

    def __init__( self, modules: Modules ):
        self.ff_states = dict(
                (m.name, False)
                for m in modules.values()
                if m.type == "%"
                )
        self.inv_inputs = dict(
                (m.name, len( m.inputs ) * [ False ])
                for m in modules.values()
                if m.type == "&"
                )


def prepare( lines: list[ str ] ) -> Modules:
    result = defaultdict( Module )
    for line in lines:
        parts = re.findall( r"(broadcaster|[%&][a-z]+) -> ([a-z]+(?:, [a-z]+)*)", line )[ 0 ]
        logic_type = parts[ 0 ][ 0 ]
        name = parts[ 0 ] if logic_type == "b" else parts[ 0 ][ 1: ]
        module = result[ name ]
        module.name = name
        module.type = logic_type
        for output in parts[ 1 ].split( ", " ):
            out_module = result[ output ]
            module.outputs[ output ] = len( out_module.inputs )
            out_module.inputs.append( name )
    return result


def task1( modules: Modules ) -> int:
    levels: dict[ bool, int ] = { False: 0, True: 0 }

    def update_level( _n, level: bool, _i ):
        levels[ level ] += 1

    sim_data: SimData = SimData( modules )
    for _ in range( 1000 ):
        simulate( modules, sim_data, update_level )
    return levels[ True ] * levels[ False ]


def task2( modules: Modules ) -> int:
    sim_data: SimData = SimData( modules )
    src_module = modules[ modules[ "rx" ].inputs[ 0 ] ]
    first_high: list[ Optional[ int ] ] = len( src_module.inputs ) * [ None ]

    def interceptor( step: int, name: str, level: bool, no: int ):
        if level and name == src_module.name:
            first_high[ no ] = step

    index = 0
    while not all( first_high ):
        index += 1
        simulate( modules, sim_data, functools.partial( interceptor, index ) )
    gcd = math.gcd( *first_high )
    lcm = reduce( lambda r, v: r * v // gcd, first_high, gcd )
    return lcm


def simulate( modules: Modules, sim_data: SimData, signal_interceptor: Callable[ [ str, bool, int ], Any ] = None ):
    signals: deque[ tuple[ str, bool, int ] ] = deque()
    signals.append( ("broadcaster", False, 0) )
    while signals:
        name, level, input_no = signals.popleft()
        if signal_interceptor:
            signal_interceptor( name, level, input_no )
        module = modules[ name ]
        match module.type:
            case "b":
                signals.extend( (out_name, level, out_no) for out_name, out_no in module.outputs.items() )
            case "%":
                if not level:
                    state = not sim_data.ff_states[ name ]
                    sim_data.ff_states[ name ] = state
                    signals.extend( (out_name, state, out_no) for out_name, out_no in module.outputs.items() )
            case "&":
                inputs = sim_data.inv_inputs[ name ]
                inputs[ input_no ] = level
                signal = not all( inputs )
                signals.extend( (out_name, signal, out_no) for out_name, out_no in module.outputs.items() )


def main():
    helper.exec_tasks(
        prepare,
        task1,
        task2,
        helper.read_file( 'data/day23_20.in' ),
        684125385,
        225872806380073
        )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        helper.print_ex( ex )
