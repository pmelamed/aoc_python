from functools import partial
from typing import Iterable

import helper
from geom2d import Coord2D, CROSS_DIRS_2D, Field2D
from helper import ignore_args, now_utc, SYM_OBSTACLE, SYM_PLANE, SYM_START
from math_helper import ap_sum

TASK2_STEPS = 26501365

PARTIALS_LONG_ROW_EXT = [
    Coord2D( 1, 3 ),
    Coord2D( 5, 3 )
]
PARTIALS_ROW_ABOVE_EXT = [
    Coord2D( 1, 2 ),
    Coord2D( 2, 2 ),
    Coord2D( 4, 2 ),
    Coord2D( 5, 2 )
]
PARTIALS_ROW_BELOW_EXT = [
    Coord2D( 1, 4 ),
    Coord2D( 2, 4 ),
    Coord2D( 4, 4 ),
    Coord2D( 5, 4 )
]
PARTIALS_TOP_ROW = [
    Coord2D( 2, 1 ),
    Coord2D( 3, 1 ),
    Coord2D( 4, 1 )
]
PARTIALS_BOTTOM_ROW = [
    Coord2D( 2, 5 ),
    Coord2D( 3, 5 ),
    Coord2D( 4, 5 )
]


class Data:
    field: Field2D[ int ]
    start_pt: Coord2D
    partials: Field2D[int]

    def __init__( self,
                  lines: list[ str ] ):
        self.field = Field2D.from_input( lines )
        self.start_pt = self.field.find( lambda _x, _y, cell: cell == SYM_START )
        self.field[ self.start_pt ] = SYM_PLANE
        self.partials = simulate_bigger_sample_field( self.field, 2 )
        print( "Partials:" )
        print( self.partials.dump() )


def task1( data: Data ) -> int:
    return len( simulate_steps( data.field, data.start_pt, 64 ) )


def task2( data: Data, overall_steps: int ) -> int:
    # We assume that overall_steps is always odd as it is in the original task
    field = data.field
    width = field.width
    height = field.height
    filled, steps_to_fill = fill_field( field, Coord2D( width - 1, height // 2 ) )
    filled_even = 0
    filled_odd = 0
    for x, y in filled.range():
        crd = Coord2D( x, y )
        if filled[ crd ]:
            if (x + y) % 2 == 0:
                filled_even += 1
            else:
                filled_odd += 1
    filled_both = filled_even + filled_odd
    print( f"""
           Fill steps- {steps_to_fill}
           Filled even - {filled_even}
           Filled odd - {filled_odd}
           Filled both - {filled_both}""" )
    partials = data.partials
    full_fields_distance = get_reach_steps( width,
                                            overall_steps,
                                            steps_to_fill )
    filled_long_row = full_fields_distance // 2 * filled_both * 2 + filled_odd
    if full_fields_distance % 2 == 1:
        filled_long_row += 2 * filled_even

    top_row = extract_field_sum( partials, PARTIALS_TOP_ROW )
    row_above = filled_long_row - filled_both + extract_field_sum( partials, PARTIALS_ROW_ABOVE_EXT )
    all_rows_above = ap_sum( first = row_above, delta = -filled_both, count = full_fields_distance )
    long_row = filled_long_row + extract_field_sum( partials, PARTIALS_LONG_ROW_EXT )
    row_below = filled_long_row - filled_both + extract_field_sum( partials, PARTIALS_ROW_BELOW_EXT )
    all_rows_below = ap_sum( first = row_below, delta = -filled_both, count = full_fields_distance )
    bottom_row = extract_field_sum( partials, PARTIALS_BOTTOM_ROW )
    print(f"""
           top_row = {top_row}
           row_above = {row_above}
           long_row = {long_row}
           row_below = {row_below}
           bottom_row = {bottom_row}""")
    return sum( [ top_row, all_rows_above, long_row, all_rows_below, bottom_row ] )


def simulate_steps( field: Field2D[ int ], start_pt: Coord2D, count: int, /, verbose = False ) -> set[ Coord2D ]:
    step: set[ Coord2D ] = { start_pt }
    prev_time = helper.now_utc()
    if verbose: print( f"Simulating {count} steps", end = "" )
    for step_idx in range( count ):
        this_time = now_utc()
        if verbose and (this_time - prev_time).total_seconds() >= 3.0:
            print( f" ... {step_idx * 100 // count}%", end = "" )
            prev_time = this_time
        step = simulate_step( field, step )
    if verbose: print( " ... finished" )
    return step


def simulate_step( field: Field2D[ int ], current_step: set[ Coord2D ] ) -> set[ Coord2D ]:
    next_step = set()
    for pts in ((npt
                 for npt in (p + d for d in CROSS_DIRS_2D)
                 if npt in field and field[ npt ] != SYM_OBSTACLE)
                for p in current_step):
        next_step.update( pts )
    return next_step


def dump_step( field: Field2D[ int ], current_step: set[ Coord2D ], diff: set[ Coord2D ] ):
    fld = field.copy()
    for pt in diff: fld[ pt ] = ord( '*' )
    for pt in current_step: fld[ pt ] = ord( 'O' )
    print( fld.dump( cell_str_f = ignore_args( 2, chr ), delim = "" ), end = "\n\n" )


def fill_field( field: Field2D[ int ], start_pt: Coord2D ) -> tuple[ Field2D[ bool ], int ]:
    step_index = 0
    front: set[ Coord2D ] = { start_pt }
    visited: Field2D[ bool ] = Field2D.from_value( field.width, field.height, False )
    visited[ start_pt ] = True
    while front:
        step_index += 1
        for pt in front:
            visited[ pt ] = True
        next_front = set()
        for pts in ((npt
                     for npt in (p + d for d in CROSS_DIRS_2D)
                     if npt in field and not visited[ npt ] and field[ npt ] != SYM_OBSTACLE)
                    for p in front):
            next_front.update( pts )
        front = next_front
    return visited, step_index


def get_reach_steps( width, overall_steps: int, steps_to_fill: int ) -> int:
    full_passed = (overall_steps - width // 2 - steps_to_fill + width) // width
    return full_passed


def simulate_bigger_sample_field( src_field: Field2D[ int ], sample_coeff: int ) -> Field2D[ int ]:
    width = src_field.width
    height = src_field.width
    steps = sample_coeff * width + width // 2
    multiplier = sample_coeff * 2 + 3
    result = Field2D.from_value( multiplier, multiplier, 0 )
    reached_pts = simulate_steps( src_field.tiles_copy( multiplier, multiplier ),
                                  Coord2D( steps + width, steps + width ),
                                  steps,
                                  verbose = True )
    for pt in reached_pts:
        result[ Coord2D( pt.x // width, pt.y // height ) ] += 1
    return result


def extract_field_sum( field: Field2D[ int ], coords: Iterable[ Coord2D ] ) -> int:
    return sum( map( field.__getitem__, coords ) )


def main():
    data = Data( helper.read_file( 'data/day23_21.in' ) )
    helper.exec_task( None,
                      partial( task2, overall_steps = 327 ),
                      data,
                      91055 )
    helper.exec_task( None,
                      partial( task2, overall_steps = 589 ),
                      data,
                      294337 )
    helper.exec_tasks( None,
                       task1,
                       partial( task2, overall_steps = TASK2_STEPS ),
                       data,
                       3542,
                       None )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        helper.print_ex( ex )
