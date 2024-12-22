from typing import Iterable

from helper import Coord, exec_tasks, print_ex, read_file

type KeyPad = dict[ tuple[ str, str ], str ]


def make_shortest_ways( keypad: dict[ str, Coord ] ) -> dict[ tuple[ str, str ], str ]:
    result = { }
    for a in keypad.items():
        for b in keypad.items():
            result[ (a[ 0 ], b[ 0 ]) ] = make_shortest_way( a[ 1 ], b[ 1 ] )
    return result


def make_shortest_way( a: Coord, b: Coord ) -> str:
    result = ""
    if a[ 1 ] < b[ 1 ]:
        result += (b[ 0 ] - a[ 0 ]) * "v"
    else:
        if a[ 1 ] > b[ 1 ]:
            result += (a[ 1 ] - b[ 1 ]) * "^"
    if a[ 0 ] < b[ 0 ]:
        result += (b[ 0 ] - a[ 0 ]) * ">"
    else:
        if a[ 0 ] > b[ 0 ]:
            result += (a[ 0 ] - b[ 0 ]) * "<"
    return result + "A"


NUM_KEYPAD: KeyPad = make_shortest_ways(
    {
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
)

CTRL_KEYPAD: KeyPad = make_shortest_ways(
    {
        "^": (1, 0),
        "A": (2, 0),
        "<": (0, 1),
        "v": (1, 1),
        ">": (2, 1)
    }
)

PADS_SEQ = (NUM_KEYPAD, CTRL_KEYPAD, CTRL_KEYPAD, CTRL_KEYPAD)


def get_press_seq( code: str, keypad: KeyPad ) -> str:
    curr = "A"
    result = ""
    for ch in code:
        result += keypad[ (curr, ch) ]
        curr = ch
    return result


def get_final_seq( code: str, pads: Iterable[ KeyPad ] ) -> str:
    result = code
    log = code
    for pad in pads:
        result = get_press_seq( result, pad )
        log += " --> " + result
    print( f"{len( result )} -- {log}" )
    return result


def get_code_value( code: str ) -> int:
    return int( code[ :-1 ], 10 )


def task1( codes: list[ str ] ) -> int:
    return sum(
        len( get_final_seq( code, PADS_SEQ ) ) * get_code_value( code )
        for code in codes
    )


def task2( codes: list[ str ] ) -> int:
    return 0


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
        None,
        None
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
