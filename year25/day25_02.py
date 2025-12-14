from helper import exec_task, print_ex, read_file


class Data:
    ranges: list[ list[ str ] ]

    def __init__( self, lines: list[ str ] ):
        pairs = lines[ 0 ].split( "," )
        self.ranges = [ p.split( "-", 2 ) for p in pairs ]


def task1( data: Data ) -> int:
    return sum( [ sum_mirrored_in_range( min_number, max_number ) for min_number, max_number in data.ranges ] )


def task2( data: Data ) -> int:
    return sum( [ sum_repeated_in_range( min_number, max_number ) for min_number, max_number in data.ranges ] )


def sum_mirrored_in_range( range_min: str, range_max: str ) -> int:
    result = 0
    min_number_len = len( range_min )
    max_number_len = len( range_max )
    for number_len in range( min_number_len, max_number_len + 1 ):
        if number_len % 2 != 0:
            continue
        result += sum_mirrored_in_len(
                number_len // 2,
                range_min if number_len == min_number_len else "1" + "0" * (number_len - 1),
                range_max if number_len == max_number_len else "9" * number_len
        )
    return result


def sum_mirrored_in_len( half_len: int, range_min: str, range_max: str ) -> int:
    min_hi = int( range_min[ :half_len ] )
    if min_hi < int( range_min[ half_len: ] ):
        min_hi += 1
    max_hi = int( range_max[ :half_len ] )
    if max_hi > int( range_max[ half_len: ] ):
        max_hi -= 1
    if min_hi > max_hi:
        return 0
    return pattern_multiplier( half_len, 2 ) * progression_sum( min_hi, max_hi )


def sum_repeated_in_range( range_min: str, range_max: str ) -> int:
    matches: set[ int ] = set()
    for number_len in range( len( range_min ), len( range_max ) + 1 ):
        len_range_min = range_min if number_len == len( range_min ) else "1" + "0" * (number_len - 1)
        len_range_max = range_max if number_len == len( range_max ) else "9" * number_len
        for pattern_size in range( 1, number_len // 2 + 1 ):
            if number_len % pattern_size != 0:
                continue
            matches.update( sum_repeated_in_pattern_len( pattern_size, len_range_min, len_range_max ) )
    result = sum( matches )
    return result


def sum_repeated_in_pattern_len(
        pattern_len: int,
        range_min: str,
        range_max: str
) -> set[ int ]:
    multiplier = pattern_multiplier( pattern_len, len( range_min ) // pattern_len )
    pattern_min = int( range_min[ :pattern_len ] )
    if pattern_min * multiplier < int( range_min ):
        pattern_min += 1
    pattern_max = int( range_max[ :pattern_len ] )
    if pattern_max * multiplier > int( range_max ):
        pattern_max -= 1
    return set( [ multiplier * pattern for pattern in range( pattern_min, pattern_max + 1 ) ] )


def progression_sum( a: int, b: int ) -> int:
    return (b - a + 1) * (a + b) // 2


def pattern_multiplier( pattern_len: int, repeats: int ) -> int:
    return int( ("1" + "0" * (pattern_len - 1)) * (repeats - 1) + "1" )


def main():
    exec_task( Data, task1, read_file( '../data/samples/year25/day25_02.sample' ), 1227775554 )
    exec_task( Data, task1, read_file( '../data/input/year25/day25_02.in' ), 32976912643 )
    exec_task( Data, task2, read_file( '../data/samples/year25/day25_02.sample' ), 4174379265 )
    exec_task( Data, task2, read_file( '../data/input/year25/day25_02.in' ), 54446379122 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
