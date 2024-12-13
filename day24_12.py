import itertools
from collections import defaultdict

from helper import Coord, CROSS_DIRS, move_forward, read_file, Direction
from helper import exec_tasks, print_ex, Field, field_from_input, field_value


def prepare( lines: list[ str ] ) -> tuple[ Field[ int ], Field[ int ], dict[ int, int ], dict[ int, str ] ]:
    field = field_from_input( lines )
    marked, squares, legend = mark_regions( field )
    return field, marked, squares, legend


def task1( data: tuple[ Field[ int ], Field[ int ], dict[ int, int ], dict[ int, str ] ] ) -> int:
    field, marked, squares, _ = data
    perimeters: dict[ int, int ] = defaultdict( lambda: 0 )

    def count_pt( this_val: int, adj_pt: Coord ):
        if not adj_pt in field:
            perimeters[ this ] += 1
        else:
            adj_val = marked[ adj_pt ]
            if this_val != adj_val:
                perimeters[ this_val ] += 1
                perimeters[ adj_val ] += 1

    for pt in itertools.product( range( field.width ), range( field.height ) ):
        this = marked[ pt ]
        count_pt( this, move_forward( pt, (1, 0) ) )
        count_pt( this, move_forward( pt, (0, 1) ) )
    for x in range( field.width ):
        perimeters[ marked[ (x, 0) ] ] += 1
    for y in range( field.height ):
        perimeters[ marked[ (0, y) ] ] += 1
    return sum( perimeters[ m ] * squares[ m ] for m in squares.keys() )


def task2( data: tuple[ Field[ int ], Field[ int ], dict[ int, int ], dict[ int, str ] ] ) -> int:
    field, marked, squares, _ = data
    sides: dict[ int, int ] = defaultdict( lambda: 0 )

    def cell( pt: Coord ) -> int:
        return marked[ pt ] if pt in marked else -1

    def scan_line( pt: Coord, dpt: Direction, dcmp: Direction ):
        region = -1
        side = False
        while pt in marked:
            pt_region = cell( pt )
            cmp_region = cell( move_forward( pt, dcmp ) )
            if pt_region != region:
                if side: sides[ region ] += 1
                region = pt_region
            else:
                if cmp_region == pt_region:
                    if side: sides[ region ] += 1
            side = pt_region != cmp_region
            pt = move_forward( pt, dpt )
        if side: sides[ region ] += 1

    for y in range( field.height ):
        scan_line( (0, y), (1, 0), (0, -1) )
        scan_line( (0, y), (1, 0), (0, 1) )
    for x in range( field.width ):
        scan_line( (x, 0), (0, 1), (-1, 0) )
        scan_line( (x, 0), (0, 1), (1, 0) )
    return sum( sides[ m ] * squares[ m ] for m in squares.keys() )


def mark_regions( field: Field[ int ] ) -> tuple[ Field[ int ], dict[ int, int ], dict[ int, str ] ]:
    marked: Field[ int ] = field_value( field.width, field.height, -1 )
    squares: dict[ int, int ] = dict()
    legend: dict[ int, str ] = dict()
    mark = 0
    for pt in itertools.product( range( field.width ), range( field.height ) ):
        if marked[ pt ] == -1:
            legend[ mark ] = chr( field[ pt ] )
            squares[ mark ] = mark_region( field, marked, pt, mark )
            mark += 1
    return marked, squares, legend


def mark_region( field: Field[ int ], marked: Field[ int ], pt: Coord, mark: int ) -> int:
    square = 1
    wave: set[ Coord ] = set()
    plant = field[ pt ]
    wave.add( pt )
    marked[ pt ] = mark
    while len( wave ) != 0:
        pt = wave.pop()
        for d in CROSS_DIRS:
            npt = move_forward( pt, d )
            if field.contains( npt ) and marked[ npt ] == -1 and field[ npt ] == plant:
                marked[ npt ] = mark
                square += 1
                wave.add( npt )
    return square


def main():
    exec_tasks( prepare, task1, task2, [ "C" ], 4, 4 )
    exec_tasks( prepare, task1, task2, read_file( 'data/day24_12.sample' ), 1930, 1206 )
    exec_tasks( prepare, task1, task2, read_file( 'data/day24_12.in' ), 1488414, 911750 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
