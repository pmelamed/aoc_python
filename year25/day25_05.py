from itertools import takewhile

from helper import exec_tasks, print_ex, read_file


class Data:
    ranges: list[ tuple[ int, int ] ]
    ids: list[ int ]

    def __init__( self, lines: list[ str ] ):
        self.ranges = sorted(
                [ parse_range( line ) for line in takewhile( lambda s: s != "", lines ) ],
                key = lambda r: r[ 0 ]
        )
        self.ids = [ int( id_str ) for id_str in lines[ len( self.ranges ) + 1: ] ]


def parse_range( line: str ) -> tuple[ int, int ]:
    return tuple( int( edge ) for edge in line.split( "-", 2 ) )


def task1( data: Data ) -> int:
    return len( [ 1 for product_id in data.ids if any( [ low <= product_id <= high for low, high in data.ranges ] ) ] )


def task2( data: Data ) -> int:
    merged: list[ tuple[ int, int ] ] = [ ]
    last_merged = data.ranges[ 0 ]
    for current_range in data.ranges[ 1: ]:
        if last_merged[ 0 ] <= current_range[ 0 ] <= last_merged[ 1 ]:
            last_merged = (last_merged[ 0 ], max( current_range[ 1 ], last_merged[ 1 ] ))
        else:
            merged.append( last_merged )
            last_merged = current_range
    merged.append( last_merged )
    return sum( hi - lo + 1 for lo, hi in merged )


def main():
    exec_tasks( Data, task1, task2, read_file( '../data/samples/year25/day25_05.sample' ), 3, 14 )
    exec_tasks( Data, task1, task2, read_file( '../data/input/year25/day25_05.in' ), 517, 336173027056994 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
