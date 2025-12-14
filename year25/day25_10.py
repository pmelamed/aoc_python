from typing import Optional
from xml.dom import InvalidStateErr

import numpy
import scipy.optimize

from helper import exec_tasks, print_ex, read_file


class Machine:
    lights: int
    button_bits: list[ int ]
    button_vals: list[ list[ int ] ]
    joltages: list[ int ]

    def __init__( self, line: str ):
        parts = line.split( ' ' )
        self.lights = Machine.parse_lights( parts[ 0 ] )
        self.joltages = Machine.parse_joltages( parts[ -1 ] )
        self.button_vals = Machine.parse_buttons_vals( parts[ 1:-1 ] )
        self.button_bits = [ Machine.make_button_bits( button ) for button in self.button_vals ]

    @staticmethod
    def parse_lights( lights_str: str ) -> int:
        return sum( 1 << idx if c == '#' else 0 for idx, c in enumerate( lights_str[ 1:-1 ] ) )

    @staticmethod
    def parse_joltages( joltages_str: str ) -> list[ int ]:
        return [ int( val_str ) for val_str in joltages_str[ 1:-1 ].split( ',' ) ]

    @staticmethod
    def parse_buttons_vals( button_strs: list[ str ] ) -> list[ list[ int ] ]:
        return [ Machine.parse_button_vals( btn_str ) for btn_str in button_strs ]

    @staticmethod
    def parse_button_vals( button_str: str ) -> list[ int ]:
        return [ int( val_str ) for val_str in button_str[ 1:-1 ].split( ',' ) ]

    @staticmethod
    def make_button_bits( button_vals: list[ int ] ) -> int:
        return sum( 1 << val for val in button_vals )


class Data:
    machines: list[ Machine ]

    def __init__( self, lines: list[ str ] ):
        self.machines = [ Machine( line ) for line in lines ]


class T1State:
    state: int
    last_button: int

    def __init__( self, state: int, last_button: int ):
        self.state = state
        self.last_button = last_button


class T2State:
    levels: list[ int ]

    def __init__( self, prev_levels: list[ int ], button_update: list[ int ] ):
        self.levels = prev_levels.copy()
        for update in button_update:
            self.levels[ update ] += 1

    def compare_levels( self, target_levels: list[ int ] ) -> int:
        result = 0
        for idx in range( len( self.levels ) ):
            if self.levels[ idx ] > target_levels[ idx ]:
                return 1
            if self.levels[ idx ] < target_levels[ idx ]:
                result = -1
        return result


def task1( data: Data ) -> int:
    return sum( get_lights_clicks( machine ) for machine in data.machines )


def task2( data: Data ) -> int:
    return int( sum( get_counters_clicks( machine ) for machine in data.machines ) )


def get_lights_clicks( machine: Machine ) -> int:
    states: list[ T1State ] = [ T1State( 0, -1 ) ]
    for depth in range( len( machine.button_bits ) ):
        next_states: list[ T1State ] = [ ]
        for state in states:
            for button_idx in range( state.last_button + 1, len( machine.button_bits ) ):
                next_state = state.state ^ machine.button_bits[ button_idx ]
                if next_state == machine.lights:
                    return depth + 1
                next_states.append( T1State( next_state, button_idx ) )
        states = next_states
    raise InvalidStateErr()


def get_counters_clicks( machine: Machine ) -> int:
    buttons_count = len( machine.button_vals )
    joltages_count = len( machine.joltages )
    c_min = numpy.array( buttons_count * [ 1 ] )
    a_eq_list = [ buttons_count * [ 0 ] for _ in range( joltages_count ) ]
    for button_idx, button_vals in enumerate( machine.button_vals ):
        for joltage_idx in button_vals:
            a_eq_list[ joltage_idx ][ button_idx ] = 1
    a_eq = numpy.array( a_eq_list )
    b_eq = numpy.array( machine.joltages )
    result = scipy.optimize.linprog( c = c_min, A_eq = a_eq, b_eq = b_eq, integrality = 1 )
    if not result.success:
        raise BaseException( "Solution not found!" )
    return sum( int( x + 0.05 ) for x in result.x )


def get_counters_by_button(
        levels: list[ int ],
        buttons: list[ list[ int ] ],
        button_idx: int
) -> Optional[ int ]:
    button = buttons[ button_idx ]
    max_number = min( levels[ idx ] for idx in button )
    update_levels( levels, button, -max_number )
    if all( levels[ i ] == 0 for i in range( len( levels ) ) ):
        update_levels( levels, button, max_number )
        return max_number
    if button_idx == len( buttons ) - 1:
        update_levels( levels, button, max_number )
        return None
    for number in range( max_number, -1, -1 ):
        deeper = get_counters_by_button( levels, buttons, button_idx + 1 )
        if deeper is not None:
            update_levels( levels, button, number )
            return deeper + number
        if number > 0:
            update_levels( levels, button, 1 )
    return None


def update_levels( levels: list[ int ], button: list[ int ], delta: int ) -> None:
    for idx in button:
        levels[ idx ] += delta


def main():
    exec_tasks( None, task1, task2, Data( read_file( '../data/samples/year25/day25_10.sample' ) ), 7, 33 )
    exec_tasks( None, task1, task2, Data( read_file( '../data/input/year25/day25_10.in' ) ), 538, 20298 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
