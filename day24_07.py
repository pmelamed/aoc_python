from collections.abc import Iterable

import helper

OP_ADD: int = 0
OP_MUL: int = 1


class Data:
    lines: [ tuple[ int, list[ int ] ] ]

    def __init__( self,
                  lines: [ int, list[ int ] ] ):
        self.lines = lines


def prepare( lines: Iterable[ str ] ) -> Data:
    data = list()
    for line in lines:
        parts: list[ str ] = line.split( ": " )
        data.append( (int( parts[ 0 ] ), [ int( val ) for val in parts[ 1 ].split( " " ) ]) )
    return Data( data )


def task1( data: Data ) -> int:
    return sum( line[ 0 ] for line in data.lines if can_be_calculated( line[ 1 ], line[ 0 ], 2 ) )


def task2( data: Data ) -> int:
    return sum( line[ 0 ] for line in data.lines if can_be_calculated( line[ 1 ], line[ 0 ], 3 ) )


def can_be_calculated( args: list[ int ], expected: int, max_op: int ) -> bool:
    ops: list[ int ] = [ 0 for _ in range( len( args ) - 1 ) ]
    while ops[ -1 ] < max_op:
        if calculate( args, ops ) == expected: return True
        index = 0
        ops[ 0 ] += 1
        while index < len( ops ) - 1 and ops[ index ] == max_op:
            ops[ index ] = 0
            ops[ index + 1 ] += 1
            index += 1
    return False


def calculate( args: list[ int ], ops: list[ int ] ) -> int:
    result = args[ 0 ]
    for op_arg in zip( ops, args[ 1: ] ):
        match op_arg[ 0 ]:
            case 0:
                result += op_arg[ 1 ]
            case 1:
                result *= op_arg[ 1 ]
            case 2:
                result = int( str( result ) + str( op_arg[ 1 ] ) )
    return result


def main():
    helper.exec_tasks( prepare, task1, task2, helper.read_file( 'data/day24_07.sample' ), 3749, 11387 )
    helper.exec_tasks( prepare, task1, task2, helper.read_file( 'data/day24_07.in' ), 303766880536, 337041851384440 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        helper.print_ex( ex )
