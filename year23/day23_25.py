import re
from collections import Counter, defaultdict

from helper import exec_task, first, print_ex, read_file


def prepare( lines: [ str ] ) -> dict[ str, set[ str ] ]:
    graf: dict[ str, set[ str ] ] = defaultdict( set )
    for idx, line in enumerate( lines ):
        src, *dst = re.split( r": | ", line )
        for node in dst:
            graf[ src ].add( node )
            graf[ node ].add( src )
    return graf


def task1( graf: dict[ str, set[ str ] ] ) -> int:
    links_counter: Counter[ str ] = Counter()
    init_node, init_links = first( graf.items() )
    group = { init_node }
    del links_counter[ init_node ]
    links_counter.update( dict( map( lambda n: (n, 1), init_links ) ) )
    while links_counter.total() > 3:
        node, _ = links_counter.most_common()[ 0 ]
        node_links = graf[ node ]
        del links_counter[ node ]
        links_counter.update( node_links - group )
        group.add( node )
    return len( group ) * (len( graf ) - len( group ))


def main():
    exec_task(
        prepare,
        task1,
        read_file( '../data/samples/year23/day23_25.sample' ),
        54
        )
    exec_task(
        prepare,
        task1,
        read_file( '../data/input/year23/day23_25.in' ),
        603368
        )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
