from helper import exec_tasks, print_ex, read_file


def task1( data: int ) -> int:
    number = data // 10
    houses: list[ int ] = number * [ 0 ]
    first_number = data * 10
    for elf in range( 1, number + 1 ):
        if elf >= first_number:
            return first_number
        for index in range( elf, number + 1, elf ):
            houses[ index - 1 ] += elf
            if houses[ index - 1 ] >= number and first_number > index:
                first_number = index
    return 0


def task2( data: int ) -> int:
    number = data // 10
    houses: list[ int ] = number * [ 0 ]
    first_number = data * 10
    for elf in range( 1, number + 1 ):
        if elf >= first_number:
            return first_number
        for index in range( elf, min( elf * 50, number ) + 1, elf ):
            houses[ index - 1 ] += elf * 11
            if houses[ index - 1 ] >= data and first_number > index:
                first_number = index
    return 0


def main():
    exec_tasks(
            lambda lines: int( lines[ 0 ] ),
            task1,
            task2,
            read_file( '../data/input/year15/day15_20.in' ),
            776160,
            786240
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
