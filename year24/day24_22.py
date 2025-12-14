from collections import defaultdict

from helper import exec_task, exec_tasks, print_ex, read_file


type Combination = tuple[ int, int, int, int ]


def prepare( lines: list[ str ] ) -> list[ int ]:
    return [ int( l ) for l in lines ]


def task1( numbers: list[ int ] ) -> int:
    return sum( gen_nth( n, 2000 ) for n in numbers )


def task2( numbers: list[ int ] ) -> int:
    gains: dict[ Combination, int ] = defaultdict( lambda: 0 )
    for number in numbers:
        process_number( number, 2000, gains )
    return max( gains.values() )


def gen_nth( number: int, n: int ) -> int:
    for _ in range( n ):
        number = gen_next( number )
    return number


def gen_next( number ):
    number = ((number << 6) ^ number) % 16777216
    number = ((number >> 5) ^ number) % 16777216
    number = ((number << 11) ^ number) % 16777216
    return number


def process_number( number: int, n: int, gain: dict[ Combination, int ] ):
    start_number = number
    log: bool = False
    already_met: set[ Combination ] = set()
    prev_val = number % 10
    combination = (None, None, None, None)
    if log:
        print( f"{number:15}: {prev_val}" )
    for _ in range( n ):
        number = gen_next( number )
        val = number % 10
        combination = (
            combination[ 1 ],
            combination[ 2 ],
            combination[ 3 ],
            (val - prev_val)
        )
        if log:
            print( f"{start_number:-6}{number:15}: {val}-{prev_val} --> {combination}" )
        if (combination[ 0 ] is not None) and (combination not in already_met):
            already_met.add( combination )
            gain[ combination ] += val
        prev_val = val


def main():
    exec_task(
            prepare,
            task1,
            [ "1", "10", "100", "2024" ],
            37327623
    )
    exec_task(
            prepare,
            task2,
            [ "1", "2", "3", "2024" ],
            23
    )
    exec_tasks(
            prepare,
            task1,
            task2,
            read_file( '../data/input/year24/day24_22.in' ),
            21147129593,
            2445
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
