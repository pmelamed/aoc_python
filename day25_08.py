import functools
import operator

from geom3d import Coord3D
from helper import exec_tasks, print_ex, read_file


class Distance:
    box1: int
    box2: int
    distance: int

    def __init__( self, box1: int, box2: int, distance: int ):
        self.box1 = box1
        self.box2 = box2
        self.distance = distance


class Data:
    boxes: list[ Coord3D ]
    distances: list[ Distance ]
    iterations: int

    def __init__( self, iterations: int, lines: list[ str ] ):
        self.boxes = [ Coord3D.from_str( line ) for line in lines ]
        self.distances = [ ]
        for idx1, box1 in enumerate( self.boxes[ :-1 ] ):
            for idx2, box2 in enumerate( self.boxes[ idx1 + 1: ] ):
                self.distances.append( Distance( idx1, idx1 + idx2 + 1, (box2 - box1).length_sqr() ) )
        self.distances.sort( key = lambda d: d.distance, reverse = False )
        self.iterations = iterations


def task1( data: Data ) -> int:
    circuits: list[ int ] = [ idx for idx in range( len( data.boxes ) ) ]
    circuit_sizes: list[ int ] = [ 1 ] * len( data.boxes )
    for distance in data.distances[ :data.iterations ]:
        box1_circuit = circuits[ distance.box1 ]
        box2_circuit = circuits[ distance.box2 ]
        if box1_circuit == box2_circuit:
            continue
        for idx, marker in enumerate( circuits ):
            if marker == box2_circuit:
                circuits[ idx ] = box1_circuit
        circuit_sizes[ box1_circuit ] += circuit_sizes[ box2_circuit ]
        circuit_sizes[ box2_circuit ] = 0
    circuit_sizes.sort( reverse = True )
    return functools.reduce( operator.imul, circuit_sizes[ :3 ], 1 )


def task2( data: Data ) -> int:
    circuits: list[ int ] = [ idx for idx in range( len( data.boxes ) ) ]
    circuit_sizes: list[ int ] = [ 1 ] * len( data.boxes )
    circuits_count = len( circuits )
    for distance in data.distances:
        box1_circuit = circuits[ distance.box1 ]
        box2_circuit = circuits[ distance.box2 ]
        if box1_circuit == box2_circuit:
            continue
        for idx, marker in enumerate( circuits ):
            if marker == box2_circuit:
                circuits[ idx ] = box1_circuit
        circuit_sizes[ box1_circuit ] += circuit_sizes[ box2_circuit ]
        circuit_sizes[ box2_circuit ] = 0
        circuits_count -= 1
        if circuits_count == 1:
            return data.boxes[ distance.box1 ].x * data.boxes[ distance.box2 ].x
    return -1


def main():
    exec_tasks( None, task1, task2, Data( 10, read_file( 'data/day25_08.sample' ) ), 40, 25272 )
    exec_tasks( None, task1, task2, Data( 1000, read_file( 'data/day25_08.in' ) ), 112230, 2573952864 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
