import functools
import operator
from typing import Callable, Iterable

from helper import exec_tasks, print_ex, read_file


class Data:
    numbers: list[ list[ int ] ]
    problems: list[ list[ int ] ]
    ops: list[ Callable[ [ Iterable[ int ] ], int ] ]

    def __init__( self, lines: list[ str ] ):
        self.numbers = [ [ int( n ) for n in line.split( " " ) if n != "" ] for line in lines[ :- 1 ] ]
        self.problems = [ ]
        problem: list[ int ] = [ ]
        for col in range( len( lines[ 0 ] ) ):
            num_str = ""
            for row in lines[ :-1 ]:
                num_str += row[ col ]
            num_str = num_str.strip()
            if num_str == "":
                self.problems.append( problem )
                problem = [ ]
            else:
                problem.append( int( num_str ) )
        if len( problem ) != 0:
            self.problems.append( problem )
        self.ops = [ operation( c ) for c in lines[ -1 ].split( " " ) if c != "" ]


def task1( data: Data ) -> int:
    return sum(
            data.ops[ index ]( row[ index ] for row in data.numbers ) for index in range( len( data.ops ) )
    )


def task2( data: Data ) -> int:
    return sum(
            data.ops[ index ]( data.problems[ index ] ) for index in range( len( data.ops ) )
    )


def operation( op_char: str ) -> Callable[ [ Iterable[ int ] ], int ]:
    return sum if op_char == "+" else lambda a: functools.reduce( operator.mul, a, 1 )


def main():
    exec_tasks( Data, task1, task2, read_file( '../data/samples/year25/day25_06.sample' ), 4277556, 3263827 )
    exec_tasks( Data, task1, task2, read_file( '../data/input/year25/day25_06.in' ), 4405895212738, 7450962489289 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
