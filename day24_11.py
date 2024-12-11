import collections

from helper import exec_task, exec_tasks, print_ex


class Data:
    stones: list[ int ]

    def __init__( self, stones: list[ int ] ):
        self.stones = stones


def prepare( lines: list[ str ] ) -> Data:
    return Data( [ int( s ) for s in lines[ 0 ].split( " " ) ] )


def task1( data: Data ) -> int:
    return process_stones( data, 25 )


def task2( data: Data ) -> int:
    return process_stones( data, 75 )


def process_stones( data, max_steps ):
    step: dict[ int, int ] = dict( zip( data.stones, len( data.stones ) * [ 1 ] ) )
    for _ in range( max_steps ):
        next_step = collections.defaultdict( lambda: 0 )
        for stone_value in step.keys():
            stones_count = step[ stone_value ]
            if stone_value == 0:
                next_step[ 1 ] += stones_count
            else:
                stone_str = str( stone_value )
                stone_len = len( stone_str )
                if stone_len % 2 == 0:
                    next_step[ int( stone_str[ : stone_len // 2 ] ) ] += stones_count
                    next_step[ int( stone_str[ stone_len // 2: ] ) ] += stones_count
                else:
                    next_step[ stone_value * 2024 ] += stones_count
        step = next_step
    return sum( step.values() )


def main():
    exec_task( prepare, task1, [ "125 17" ], 55312 )
    exec_tasks( prepare, task1, task2, [ "4189 413 82070 61 655813 7478611 0 8" ], 186203, 221291560078593 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
