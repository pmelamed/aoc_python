from collections import defaultdict
from itertools import batched

from helper import exec_task, print_ex, read_file


type Pattern = tuple[ int, ... ]


class Data:
    keys: list[ Pattern ]
    locks: list[ Pattern ]

    def __init__( self, lines: list[ str ] ):
        self.graph = defaultdict( set )
        self.keys = list()
        self.locks = list()
        for schema in batched( filter( lambda l: l != "", lines ), 7 ):
            pattern: list[ int ] = [ 0, 0, 0, 0, 0 ]
            for line in schema[ 1:6 ]:
                for index, ch in enumerate( line ):
                    if ch == "#":
                        pattern[ index ] += 1
            if schema[ 0 ] == "#####":
                self.locks.append( tuple( pattern ) )
            else:
                self.keys.append( tuple( pattern ) )


def task1( data: Data ) -> int:
    count = 0
    for key in data.keys:
        for lock in data.locks:
            if is_key_fit( key, lock ):
                count += 1
    return count


def task2( data: Data ) -> int:
    return 0


def is_key_fit( key: Pattern, lock: Pattern ) -> bool:
    for pair in zip( key, lock ):
        if pair[ 0 ] + pair[ 1 ] > 5:
            return False
    return True


def main():
    exec_task(
            Data,
            task1,
            read_file( '../data/samples/year24/day24_25.sample' ),
            3
    )
    exec_task(
            Data,
            task1,
            read_file( '../data/input/year24/day24_25.in' ),
            3320
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
