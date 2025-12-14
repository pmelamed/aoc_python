from functools import cmp_to_key

from helper import exec_tasks, print_ex, read_file


class Data:
    towels: list[ str ]
    designs: list[ str ]

    def __init__( self, towels: list[ str ], designs: list[ str ] ):
        self.towels = towels
        self.towels.sort( key = cmp_to_key( lambda a, b: len( a ) - len( b ) ) )
        self.designs = designs


def prepare( lines: list[ str ] ) -> Data:
    return Data( lines[ 0 ].split( ", " ), lines[ 2: ] )


def task1( data: Data ) -> int:
    return sum( 1 for design in data.designs if try_assemble( design, data.towels ) )


def task2( data: Data ) -> int:
    combs: dict[ str, int ] = { }
    result = sum( count_assembles( combs, design, data.towels ) for design in data.designs )
    return result


def try_assemble( design: str, towels: list[ str ] ) -> bool:
    for towel in towels:
        design_len = len( design )
        towel_len = len( towel )
        if design_len < towel_len:
            continue
        if design_len == towel_len:
            if design == towel:
                return True
            else:
                continue
        if (design[ :towel_len ] == towel
                and try_assemble( design[ towel_len: ], towels )):
            return True
    return False


def count_assembles( combinations: dict[ str, int ], design: str, towels: list[ str ] ) -> int:
    if design == "":
        return 1
    if design in combinations:
        return combinations[ design ]
    result = 0
    design_len = len( design )
    for towel in towels:
        towel_len = len( towel )
        if design_len < towel_len:
            break
        if design[ :towel_len ] == towel:
            result += count_assembles( combinations, design[ towel_len: ], towels )
    combinations[ design ] = result
    return result


def main():
    exec_tasks(
            prepare,
            task1,
            task2,
            read_file( '../data/samples/year24/day24_19.sample' ),
            6,
            16
    )
    exec_tasks(
            prepare,
            task1,
            task2,
            read_file( '../data/input/year24/day24_19.in' ),
            263,
            723524534506343
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
