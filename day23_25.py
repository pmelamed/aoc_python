import re
from collections import Counter, defaultdict, deque

from helper import exec_task, first, print_ex, read_file


class Data:
    graf: dict[ str, set[ str ] ]
    links: list[ tuple[ str, str ] ]

    def __init__( self, lines: [ str ] ):
        graf: dict[ str, set[ str ] ] = defaultdict( set )
        links: list[ tuple[ str, str ] ] = [ ]
        for idx, line in enumerate( lines ):
            src, *dst = re.split( r": | ", line )
            for node in dst:
                graf[ src ].add( node )
                graf[ node ].add( src )
                links.append( (src, node) )
        self.graf = graf
        self.links = links


def task1( data: Data ) -> int:
    graf = data.graf
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


def build_linked_group( graf: dict[ str, set[ str ] ], dropped: list[ tuple[ str, str ] ] ) -> int:
    start_node = dropped[ 0 ][ 0 ]
    queue: deque[ str ] = deque( [ start_node ] )
    group: set[ str ] = { start_node }
    while queue:
        node = queue.popleft()
        for nxt in graf[ node ] - group:
            if nxt == dropped[ 0 ][ 1 ]: return -1
            queue.append( nxt )
            group.add( nxt )
    return len( group )


def main():
    exec_task( Data,
               task1,
               read_file( 'data/day23_25.sample' ),
               54 )
    exec_task( Data,
               task1,
               read_file( 'data/day23_25.in' ),
               603368 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
