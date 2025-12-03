from numpy import argmax

from helper import exec_task, print_ex, read_file


class Data:
    banks: list[ list[ int ] ]

    def __init__( self, lines: list[ str ] ):
        self.banks = [ [ int( ch ) for ch in bank ] for bank in lines ]


def task1( data: Data ) -> int:
    return sum( [ find_max_capacity_n( bank, 2 ) for bank in data.banks ] )


def task2( data: Data ) -> int:
    return sum( [ find_max_capacity_n( bank, 12 ) for bank in data.banks ] )


def print_max_capacity( bank: list[ int ], max_capacity: int ) -> int:
    print( f"{max_capacity} <- {bank}" )
    return max_capacity


def find_max_capacity( bank: list[ int ] ) -> int:
    hi_index = argmax( bank[ : -1 ] )
    lo_index = argmax( bank[ hi_index + 1: ] )
    return bank[ hi_index ] * 10 + bank[ hi_index + lo_index + 1 ]


def find_max_capacity_n( bank: list[ int ], num_batteries: int ) -> int:
    result = 0
    hi_index = 0
    for battery_index in range( num_batteries - 1 ):
        next_hi_index = argmax( bank[ hi_index:-(num_batteries - battery_index - 1) ] )
        result = result * 10 + bank[ hi_index + next_hi_index ]
        hi_index = hi_index + next_hi_index + 1
    next_hi_index = argmax( bank[ hi_index: ] )
    return result * 10 + bank[ hi_index + next_hi_index ]


def main():
    exec_task( Data, task1, read_file( 'data/day25_03.sample' ), 357 )
    exec_task( Data, task1, read_file( 'data/day25_03.in' ), 17332 )
    exec_task( Data, task2, read_file( 'data/day25_03.sample' ), 3121910778619 )
    exec_task( Data, task2, read_file( 'data/day25_03.in' ), 172516781546707 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
