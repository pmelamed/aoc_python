from helper import exec_task, exec_tasks, print_ex, read_file


class Data:
    connections: dict[ str, list[ str ] ]

    def __init__( self, lines: list[ str ] ):
        self.connections = dict( [ (line.split( ":" )[ 0 ], line.split( ": " )[ 1 ].split( " " )) for line in lines ] )
        self.connections[ "out" ] = [ ]


def task1( data: Data ) -> int:
    return find_all_paths_between( data.connections, "you", "out" )


def task2( data: Data ) -> int:
    return ((find_all_paths_between( data.connections, "svr", "dac" ) *
             find_all_paths_between( data.connections, "dac", "fft" ) *
             find_all_paths_between( data.connections, "fft", "out" )) +
            (find_all_paths_between( data.connections, "svr", "fft" ) *
             find_all_paths_between( data.connections, "fft", "dac" ) *
             find_all_paths_between( data.connections, "dac", "out" )))


def find_all_paths_between( connections: dict[ str, list[ str ] ], node_from: str, node_to: str ) -> int:
    mem: dict[ str, int ] = { node_to: 1 }
    return find_all_paths( connections, node_from, mem )


def find_all_paths( connections: dict[ str, list[ str ] ], node: str, mem: dict[ str, int ] ) -> int:
    paths_count = mem.get( node )
    if paths_count is not None:
        return paths_count
    paths_count = sum( find_all_paths( connections, out, mem ) for out in connections[ node ] )
    mem[ node ] = paths_count
    return paths_count


def main():
    exec_task( Data, task1, read_file( '../data/samples/year25/day25_11_1.sample' ), 5 )
    exec_task( Data, task2, read_file( '../data/samples/year25/day25_11_2.sample' ), 2 )
    exec_tasks( Data, task1, task2, read_file( '../data/input/year25/day25_11.in' ), 534, 499645520864100 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
