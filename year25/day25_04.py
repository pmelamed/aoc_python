from geom2d import Coord2D, Field2D, Rect2D, STAR_DIRS_2D
from helper import exec_task, print_ex, read_file


class Data:
    field: Field2D[ bool ]
    actual_rect: Rect2D

    def __init__( self, lines: list[ str ] ):
        width = len( lines[ 0 ] )
        height = len( lines )
        self.actual_rect = Rect2D.from_coords( 1, 1, width + 1, height + 1 )
        self.field = Field2D.from_generate(
                width + 2,
                height + 2,
                lambda coord: 0 < coord.x <= width
                              and 0 < coord.y <= height
                              and lines[ coord.y - 1 ][ coord.x - 1 ] == '@'
        )


def task1( data: Data ) -> int:
    return data.field.count_if(
            # lambda x, y, cell: debug_t1( data, x, y, cell )
            lambda x, y, cell: cell and data.actual_rect.contains( Coord2D.from_coords( x, y ) )
                               and data.field.count_around(
                    Coord2D.from_coords( x, y ), lambda a: a, STAR_DIRS_2D
            ) < 4
    )


def task2( data: Data ) -> int:
    count = 0
    while True:
        to_remove = [
            Coord2D.from_coords( x, y )
            for x, y, _ in data.field.filter(
                    lambda x, y, cell: cell and data.actual_rect.contains( Coord2D.from_coords( x, y ) )
                                       and data.field.count_around(
                        Coord2D.from_coords( x, y ), lambda a: a, STAR_DIRS_2D
                        ) < 4
            )
        ]
        remove_count = len( to_remove )
        if remove_count == 0:
            return count
        count += remove_count
        for coord in to_remove:
            data.field[ coord ] = False


def main():
    sample = Data( read_file( '../data/samples/year25/day25_04.sample' ) )
    task = Data( read_file( '../data/input/year25/day25_04.in' ) )
    exec_task( None, task1, sample, 13 )
    exec_task( None, task1, task, 1433 )
    exec_task( None, task2, sample, 43 )
    exec_task( None, task2, task, 8616 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
