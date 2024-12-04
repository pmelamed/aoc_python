import helper


class Data:
    def __init__( self ):
        pass


def task1( lines: list[ str ] ) -> int:
    y_len = len( lines )
    x_len = len( lines[ 0 ] )
    result: int = 0
    for dx, dy in [ (-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1) ]:
        x_from = max( 0, -dx * 4 - 1 )
        x_to = min( x_len, x_len - dx * 4 + 1 )
        y_from = max( 0, -dy * 4 - 1 )
        y_to = min( y_len, y_len - dy * 4 + 1 )
        result += check_range( lines, x_from, x_to, y_from, y_to, dx, dy )
    return result


def task2( lines: list[ str ] ) -> int:
    return len( [ 1 \
                  for y in range( 1, len( lines ) - 1 ) \
                  for x in range( 1, len( lines[ 0 ] ) - 1 ) \
                  if lines[ y ][ x ] == "A" and \
                  check_line( lines[ y - 1 ][ x - 1 ], lines[ y + 1 ][ x + 1 ] ) and \
                  check_line( lines[ y - 1 ][ x + 1 ], lines[ y + 1 ][ x - 1 ] ) ] )


def check_range( lines: list[ str ], x_from: int, x_to: int, y_from: int, y_to: int, dx: int, dy: int ) -> int:
    return sum( [ check_entry( lines, x, y, dx, dy ) for y in range( y_from, y_to ) for x in range( x_from, x_to ) ] )


def check_entry( lines: list[ str ], x: int, y: int, dx: int, dy: int ) -> int:
    if lines[ y ][ x ] == 'X' \
            and lines[ y + dy ][ x + dx ] == 'M' \
            and lines[ y + 2 * dy ][ x + 2 * dx ] == 'A' and \
            lines[ y + 3 * dy ][ x + 3 * dx ] == 'S':
        return 1
    return 0


def check_line( ch1: str, ch2: str ) -> bool:
    return ch1 == "M" and ch2 == "S" or \
        ch1 == "S" and ch2 == "M"


if __name__ == '__main__':
    try:
        helper.exec_tasks( None, task1, task2, helper.read_file( 'data/day04.sample' ), 18, 9 )
        helper.exec_tasks( None, task1, task2, helper.read_file( 'data/day04.in' ), 2493, None )
    except Exception as ex:
        helper.print_ex( ex )
