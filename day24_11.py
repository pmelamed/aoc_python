import helper
from helper import exec_tasks, read_file, print_ex


class Data:
    stones: list[ str ]

    def __init__( self, stones: list[ str ] ):
        self.stones = stones


def prepare( lines: list[ str ] ) -> Data:
    return Data( lines[ 0 ].split( " " ) )


def task1( data: Data ) -> int:
    return process_stones( data, 25 )


def task2( data: Data ) -> int:
    return process_stones( data, 75 )


def process_stones( data, max_steps ):
    return sum( process_stone( stone, 0, max_steps ) for stone in data.stones )


def process_stone( stone: str, steps: int, max_steps: int ) -> int:
    if steps == max_steps: return 1
    if stone == "0": return process_stone( "1", steps + 1, max_steps )
    if len(stone) > 1 and len( stone ) % 2 == 0:
        return process_stone( str( int( stone[ : len( stone ) // 2 ] ) ), steps + 1, max_steps ) + \
            process_stone( str( int( stone[ len( stone ) // 2: ] ) ), steps + 1, max_steps )
    return process_stone( str( int( stone ) * 2024 ), steps + 1, max_steps )


def main():
    helper.exec_task( prepare, task1,  [ "125 17" ], 55312 )
    exec_tasks( prepare, task1, task2, [ "4189 413 82070 61 655813 7478611 0 8" ], 186203, None )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
