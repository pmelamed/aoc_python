import re
from collections.abc import Iterable

import helper

INSTRUCTION_REGEXP = "(do\\(\\)|don\'t\\(\\)|mul\\(([1-9][0-9]{0,2}),([1-9][0-9]{0,2})\\))"

def task1( data: Iterable[ str ] ) -> int:
    return calc_row( " ".join( data ) )


def task2( data: Iterable[ str ] ) -> int:
    return calc_row2( " ".join( data ) )


def calc_row( row: str ) -> int:
    return sum(
        [ instruction( entry )
          for entry in re.findall( INSTRUCTION_REGEXP, row )
          if entry[ 0 ][ 0:3 ] == "mul" ]
    )


def instruction( entry: tuple[ str, str, str ] ) -> int:
    return int( entry[ 1 ] ) * int( entry[ 2 ] )


def calc_row2( row: str ) -> int:
    enabled: bool = True
    result: int = 0
    for entry in re.findall( INSTRUCTION_REGEXP, row ):
        match entry[ 0 ]:
            case "don't()":
                enabled = False
            case "do()":
                enabled = True
            case _:
                if enabled: result += instruction( entry )
    return result


if __name__ == '__main__':
    try:
        helper.exec_task(
            None,
            task1,
            [ "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))" ],
            161
        )
        helper.exec_task(
            None,
            task2,
            [ "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))" ],
            48
        )
        helper.exec_tasks(
            None,
            task1,
            task2,
            helper.read_file( 'data/day03.in' ),
            175615763,
            74361272 )
    except Exception as ex:
        helper.print_ex( ex )
