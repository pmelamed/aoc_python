import functools
import itertools
from collections.abc import Iterable

import helper


class Data:
    preceding_pages: dict[ int, set[ int ] ]
    samples: list[ tuple[ int, ... ] ]

    def __init__( self, preceding_pages: dict[ int, set[ int ] ], samples: list[ tuple[ int, ... ] ] ):
        self.preceding_pages = preceding_pages
        self.samples = samples
        pass


def prepare( lines: Iterable[ str ] ) -> Data:
    preceding_sets = dict()
    for pair in map( split_pair, itertools.takewhile( helper.not_empty_str_predicate, lines ) ):
        preceding_sets.setdefault( pair[ 1 ], set() ).add( pair[ 0 ] )
    samples = [ split_pages( s )
                for s in itertools.islice( itertools.dropwhile( helper.not_empty_str_predicate, lines ), 1, None ) ]
    return Data( preceding_sets, samples )


def task1( data: Data ) -> int:
    return sum( [ check_sample( sample, data ) for sample in data.samples ] )


def task2( data: Data ) -> int:
    return sum( [ fix_sample( sample, data ) for sample in data.samples if not check_sample( sample, data ) ] )


def split_pair( s: str ) -> tuple[ int, ... ]:
    return tuple( map( int, s.split( "|", 2 ) ) )


def split_pages( s: str ) -> tuple[ int, ... ]:
    return tuple( map( int, s.split( "," ) ) )


def check_sample( sample: tuple[ int, ... ], data: Data ) -> int:
    prohibited: set[ int ] = set( { } )
    for page in sample:
        if page in prohibited:
            return 0
        preceding = data.preceding_pages.get( page )
        if preceding is not None:
            prohibited.update( preceding )
    return sample[ len( sample ) // 2 ]


def fix_sample( sample: tuple[ int, ... ], data: Data ) -> int:
    fixed = list( sample )

    def cmp_fn( page1: int, page2: int ) -> int:
        page1_preceding = data.preceding_pages.get( page1 )
        page2_preceding = data.preceding_pages.get( page2 )
        if page1_preceding is not None and page2 in page1_preceding:
            return 1
        if page2_preceding is not None and page1 in page2_preceding:
            return -1
        return 0

    fixed = sorted( fixed, key = functools.cmp_to_key( cmp_fn ) )
    return fixed[ len( sample ) // 2 ]


def main():
    helper.exec_tasks( prepare, task1, task2, helper.read_file( 'data/day24_05.sample' ), 143, 123 )
    helper.exec_tasks( prepare, task1, task2, helper.read_file( 'data/day24_05.in' ), 5087, 4971 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        helper.print_ex( ex )
