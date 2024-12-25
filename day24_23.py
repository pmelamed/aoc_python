from collections import defaultdict

from helper import exec_tasks, print_ex, read_file

type Graph = dict[ str, set[ str ] ]


class Data:
    graph: Graph

    def __init__( self, lines: list[ str ] ):
        self.graph = defaultdict( set )
        for line in lines:
            nodes = line.split( "-" )
            self.graph[ nodes[ 0 ] ].add( nodes[ 1 ] )
            self.graph[ nodes[ 1 ] ].add( nodes[ 0 ] )


def task1( data: Data ) -> int:
    count: int = 0
    t_nodes = sorted( node for node in data.graph.keys() if node[ 0 ] == 't' )
    for t_node in t_nodes:
        vertex = list( data.graph[ t_node ] )
        for idx1 in range( len( vertex ) - 1 ):
            vertice1 = vertex[ idx1 ]
            if vertice1[ 0 ] == 't' and vertice1 < t_node: continue
            peer_vertex = data.graph[ vertice1 ]
            for idx2 in range( idx1 + 1, len( vertex ) ):
                vertice2 = vertex[ idx2 ]
                if vertice2[ 0 ] == 't' and vertice2 < t_node: continue
                if vertice2 in peer_vertex:
                    count += 1
    return count


def task2( data: Data ) -> str:
    largest: set[ str ] = set()
    for node, vertex in data.graph.items():
        node_largest = get_largest_append(
            data.graph,
            { node },
            [ v for v in vertex if v > node ]
        )
        if len( node_largest ) > len( largest ): largest = node_largest
    return ",".join( sorted( list( largest ) ) )


def get_largest_append( graph: Graph, added: set[ str ], candidates: list[ str ] ) -> set[ str ]:
    if len( candidates ) == 0:
        return added.copy()
    largest: set[ str ] = set()
    for index in range( len( candidates ) ):
        candidate = candidates[ index ]
        if can_append( graph, added, candidate ):
            added.add( candidate )
            new_largest = get_largest_append( graph, added, candidates[ index + 1: ] )
            if len( new_largest ) > len( largest ): largest = new_largest
            added.remove( candidate )
    return largest


def can_append( graph: Graph, existing: set[ str ], candidate: str ) -> bool:
    return all( node in graph[ candidate ] for node in existing )


def main():
    exec_tasks(
        Data,
        task1,
        task2,
        read_file( 'data/day24_23.sample' ),
        7,
        "co,de,ka,ta"
    )
    exec_tasks(
        Data,
        task1,
        task2,
        read_file( 'data/day24_23.in' ),
        1400,
        "am,bc,cz,dc,gy,hk,li,qf,th,tj,wf,xk,xo"
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
