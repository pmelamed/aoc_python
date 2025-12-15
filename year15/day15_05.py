from helper import count_if, exec_tasks, print_ex, read_file


def task1( data: list[ str ] ) -> int:
    return count_if( is_nice, data )


def task2( data: list[ str ] ) -> int:
    return count_if( is_nice2, data )


def is_nice( s: str ) -> bool:
    flag_double = False
    flag_vowels = 0
    for idx in range( len( s ) - 1 ):
        if s[ idx ] == s[ idx + 1 ]:
            flag_double = True
        if s[ idx ] in 'aeiou':
            flag_vowels += 1
        if s[ idx ] + s[ idx + 1 ] in { "ab", "cd", "pq", "xy" }:
            return False
    if s[ -1 ] in 'aeiou':
        flag_vowels += 1
    return flag_vowels >= 3 and flag_double


def is_nice2( s: str ) -> bool:
    pairs: dict[ str, int ] = { }
    flag_double = False
    flag_triple = False
    for idx in range( len( s ) - 1 ):
        if idx + 2 < len( s ) and s[ idx ] == s[ idx + 2 ]:
            flag_triple = True
        dbl = s[ idx ] + s[ idx + 1 ]
        if dbl in pairs:
            flag_double = flag_double or idx - pairs[ dbl ] > 1
        else:
            pairs[ dbl ] = idx
    return flag_double and flag_triple


def main():
    exec_tasks( None, task1, task2, read_file( '../data/input/year15/day15_05.in' ), 255, 55 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
