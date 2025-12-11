from helper import exec_tasks, print_ex, read_file


class Data:
    connections: dict[ str, list[ str ] ]

    def __init__( self, lines: list[ str ] ):
        self.connections = dict( [ (line.split( ":" )[ 0 ], line.split( ": " )[ 1 ].split( " " )) for line in lines ] )


def task1( data: Data ) -> int:
    mem: dict[ str, int ] = { "out": 1 }
    return find_all_paths( data.connections, "you", mem )


def find_all_paths( connections: dict[ str, list[ str ] ], node: str, mem: dict[ str, int ] ) -> int:
    paths_count = mem.get( node )
    if paths_count is not None:
        return paths_count
    paths_count = sum( find_all_paths( connections, out, mem ) for out in connections[ node ] )
    mem[ node ] = paths_count
    return paths_count


def task2( data: Data ) -> int:
    return 0


def main():
    exec_tasks( Data, task1, task2, read_file( 'data/day25_11.sample' ), 5, None )
    exec_tasks( Data, task1, task2, read_file( 'data/day25_11.in' ), None, None )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
