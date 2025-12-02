from collections import deque
from itertools import pairwise, product
from typing import Optional

from helper import Coord, Field, exec_task, exec_tasks, field_value, inside_rect, move_forward, print_ex, read_file


type KeyPadMoves = dict[ tuple[ str, str ], int ]
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

HUMAN_KEYPAD_MOVES: KeyPadMoves = dict( ((a, b), 1) for a, b in product( "^<v>A", repeat = 2 ) )

DIR_CHARS = {
    "<": (-1, 0),
    ">": (1, 0),
    "^": (0, -1),
    "v": (0, 1)
}


def task1( codes: list[ str ] ) -> int:
    moves = HUMAN_KEYPAD_MOVES
    for _ in range( 2 ):
        moves = get_optimal_moves( CTRL_KEYPAD_LAYOUT, CTRL_KEYPAD_SIZE, CTRL_KEYPAD_GAP, moves )
    moves = get_optimal_moves( NUM_KEYPAD_LAYOUT, NUM_KEYPAD_SIZE, NUM_KEYPAD_GAP, moves )
    return sum(
            get_press_seq( code, moves ) * get_code_value( code )
            for code in codes
    )


def task2( codes: list[ str ] ) -> int:
    moves = HUMAN_KEYPAD_MOVES
    for _ in range( 25 ):
        moves = get_optimal_moves( CTRL_KEYPAD_LAYOUT, CTRL_KEYPAD_SIZE, CTRL_KEYPAD_GAP, moves )
    moves = get_optimal_moves( NUM_KEYPAD_LAYOUT, NUM_KEYPAD_SIZE, NUM_KEYPAD_GAP, moves )
    return sum(
            get_press_seq( code, moves ) * get_code_value( code )
            for code in codes
    )


def get_code_value( code: str ) -> int:
    return int( code[ :-1 ], 10 )


def get_press_seq( code: str, keypad: KeyPadMoves ) -> int:
    return sum( keypad[ (a, b) ] for a, b in pairwise( "A" + code ) )


def get_optimal_moves(
        dst_layout: KeyPadLayout,
        dst_size: Coord,
        dst_gap: Optional[ Coord ],
        ctrl_moves: KeyPadMoves
        ) -> KeyPadMoves:
    return dict(
            ((a, b), get_optimal_way( dst_layout[ a ], dst_layout[ b ], dst_size, dst_gap, ctrl_moves ))
            for a, b in product( dst_layout.keys(), repeat = 2 )
            )


def get_optimal_way( a: Coord, b: Coord, size: Coord, gap: Optional[ Coord ], moves: KeyPadMoves ) -> int:
    max_way_length = size[ 0 ] * size[ 1 ] * max( s for s in moves.values() ) + 1
    min_way_len = max_way_length
    field_rect = (0, 0, size[ 0 ], size[ 1 ])
    passed: dict[ str, Field[ int ] ] = dict(
            (key, field_value( size[ 0 ], size[ 1 ], max_way_length ))
            for key in DIR_CHARS
            )
    passed[ "A" ] = field_value( size[ 0 ], size[ 1 ], max_way_length )
    if gap is not None:
        for key in passed:
            passed[ key ][ gap ] = -1
    wave = deque[ tuple[ Coord, int, str ] ]()
    wave.append( (a, 0, "A") )
    while wave:
        pt, length, last_dir = wave.popleft()
        if not inside_rect( pt, field_rect ) or passed[ last_dir ][ pt ] < length:
            continue
        if pt == b:
            full_way_len = length + moves[ (last_dir, "A") ]
            if full_way_len < min_way_len:
                min_way_len = full_way_len
            continue
        passed[ last_dir ][ pt ] = length
        wave.extend(
                (move_forward( pt, d_vector ), length + moves[ (last_dir, d_char) ], d_char)
                for d_char, d_vector in DIR_CHARS.items()
                )
    return min_way_len


def main():
    exec_task(
            None,
            task1,
            read_file( 'data/day24_21.sample' ),
            126384
    )
    exec_tasks(
            None,
            task1,
            task2,
            read_file( 'data/day24_21.in' ),
            176870,
            223902935165512
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
