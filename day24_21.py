from collections import deque
from itertools import pairwise, product
from typing import Optional

from helper import Coord, exec_tasks, Field, field_value, move_forward, print_ex, read_file

type KeyPadMoves = dict[ tuple[ str, str ], str ]
type KeyPadLayout = dict[ str, Coord ]

NUM_KEYPAD_LAYOUT: KeyPadLayout = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "0": (1, 3),
    "A": (2, 3)
}
NUM_KEYPAD_SIZE = (3, 4)
NUM_KEYPAD_GAP = (0, 3)

CTRL_KEYPAD_LAYOUT: KeyPadLayout = {
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1)
}
CTRL_KEYPAD_SIZE = (3, 2)
CTRL_KEYPAD_GAP = (0, 0)

HUMAN_KEYPAD_MOVES: KeyPadMoves = dict( ((a, b), b) for a, b in product( "^<v>A", repeat = 2 ) )

DIR_CHARS = {
    "<": (-1, 0),
    ">": (1, 0),
    "^": (0, -1),
    "v": (0, 1)
}


def task1( codes: list[ str ] ) -> int:
    human_moves = get_optimal_moves( CTRL_KEYPAD_LAYOUT, CTRL_KEYPAD_SIZE, CTRL_KEYPAD_GAP, HUMAN_KEYPAD_MOVES )
    # print( f" Human = {human_moves}" )
    robot1_moves = get_optimal_moves( CTRL_KEYPAD_LAYOUT, CTRL_KEYPAD_SIZE, CTRL_KEYPAD_GAP, human_moves )
    # print( f" Robot #1 = {robot1_moves}" )
    robot2_moves = get_optimal_moves( NUM_KEYPAD_LAYOUT, NUM_KEYPAD_SIZE, NUM_KEYPAD_GAP, robot1_moves )
    # print( f" Robot #3 = {robot2_moves}" )
    # results = list( (get_code_value( code ),
    #                  get_press_seq( code, robot2_moves ),
    #                  len( get_press_seq( code, robot2_moves ) ))
    #                 for code in codes )
    # print( results )
    # for _1, seq, _2 in results:
    #     print( seq )
    #     seq = emulate( seq, CTRL_KEYPAD_LAYOUT )
    #     print( seq )
    #     seq = emulate( seq, CTRL_KEYPAD_LAYOUT )
    #     print( seq )
    #     seq = emulate( seq, NUM_KEYPAD_LAYOUT )
    #     print( seq )
    return sum(
        len( get_press_seq( code, robot2_moves ) ) * get_code_value( code )
        for code in codes
    )


def task2( codes: list[ str ] ) -> int:
    moves = HUMAN_KEYPAD_MOVES
    for _ in range(25):
        moves = get_optimal_moves( CTRL_KEYPAD_LAYOUT, CTRL_KEYPAD_SIZE, CTRL_KEYPAD_GAP, moves )
    moves = get_optimal_moves( NUM_KEYPAD_LAYOUT, NUM_KEYPAD_SIZE, NUM_KEYPAD_GAP, moves )
    return sum(
        len( get_press_seq( code, moves ) ) * get_code_value( code )
        for code in codes
    )


def get_code_value( code: str ) -> int:
    return int( code[ :-1 ], 10 )


def get_press_seq( code: str, keypad: KeyPadMoves ) -> str:
    return "".join( keypad[ (a, b) ] for a, b in pairwise( "A" + code ) )


def get_optimal_moves( dst_layout: KeyPadLayout,
                       dst_size: Coord,
                       dst_gap: Optional[ Coord ],
                       ctrl_moves: KeyPadMoves ) -> KeyPadMoves:
    return dict( ((a, b), get_optimal_way( dst_layout[ a ], dst_layout[ b ], dst_size, dst_gap, ctrl_moves ))
                 for a, b in product( dst_layout.keys(), repeat = 2 ) )


def get_optimal_way( a: Coord, b: Coord, size: Coord, gap: Optional[ Coord ], moves: KeyPadMoves ) -> str:
    max_way_length = size[ 0 ] * size[ 1 ] * max( len( s ) for s in moves.values() ) + 1
    min_way = None
    min_way_len = max_way_length
    passed: Field[ int ] = field_value( size[ 0 ], size[ 1 ], max_way_length )
    if gap is not None: passed[ gap ] = -1
    wave = deque[ tuple[ Coord, str, str ] ]()
    wave.append( (a, "", "A") )
    while wave:
        pt, way, last_dir = wave.popleft()
        if pt not in passed or passed[ pt ] < len( way ): continue
        if pt == b:
            full_way = way + moves[ (last_dir, "A") ]
            full_way_len = len( full_way )
            if full_way_len < min_way_len:
                min_way = full_way
                min_way_len = full_way_len
            continue
        passed[ pt ] = len( way )
        wave.extend( (move_forward( pt, d_vector ), way + moves[ (last_dir, d_char) ], d_char)
                     for d_char, d_vector in DIR_CHARS.items() )
    return min_way


def emulate( moves: str, layout: KeyPadLayout ) -> str:
    pt = layout[ "A" ]
    result = ""
    for move in moves:
        if move == "A":
            result += next( key for key in layout if layout[ key ] == pt )
        else:
            pt = move_forward( pt, DIR_CHARS[ move ] )
    return result


def main():
    exec_tasks(
        None,
        task1,
        task2,
        read_file( 'data/day24_21.sample' ),
        126384,
        None
    )
    exec_tasks(
        None,
        task1,
        task2,
        read_file( 'data/day24_21.in' ),
        176870,
        None
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
