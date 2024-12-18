import functools

from helper import Coord, CROSS_DIRS, exec_tasks, Field, field_value, print_ex, read_file

type Drops = list[ Coord ]


class Data:
    drops: Drops
    drops_count: int
    field: Field[ int ]

    def __init__( self, field: Field[ int ], drops: Drops, drops_count: int ):
        self.drops = drops
        self.drops_count = drops_count
        self.field = field


EMPTY = ord( '.' )
OBSTACLE = ord( '#' )


def prepare( lines: list[ str ], dim: int, drops_count: int ) -> Data:
    field = field_value( dim + 2, dim + 2, ord( "." ) )
    for x in range( dim + 2 ):
        field[ (x, 0) ] = OBSTACLE
        field[ (x, field.height - 1) ] = OBSTACLE
    for y in range( dim + 2 ):
        field[ (0, y) ] = OBSTACLE
        field[ (field.width - 1, y) ] = OBSTACLE
    return Data(
        field,
        [ (int( c[ 0 ] ) + 1, int( c[ 1 ] ) + 1) for c in map( lambda l: l.split( "," ), lines ) ],
        drops_count
    )


def task1( data: Data ) -> int:
    field = data.field
    for addr in data.drops[ :data.drops_count ]:
        field[ addr ] = OBSTACLE
    way_field = field_value( field.width, field.height, field.width * field.height )
    wave = [ (1, 1, 0) ]
    while wave:
        x, y, l = wave.pop()
        pt = (x, y)
        if field[ pt ] == OBSTACLE or way_field[ pt ] <= l: continue
        way_field[ pt ] = l
        for d in CROSS_DIRS: wave.append( (x + d[ 0 ], y + d[ 1 ], l + 1) )
    return way_field[ field.width - 2, field.height - 2 ]


def task2( data: Data ) -> str:
    field = data.field
    for addr in data.drops[ data.drops_count: ]:
        field[ addr ] = OBSTACLE
        if not is_accessible( field ): return f"{addr[ 0 ] - 1},{addr[ 1 ] - 1}";
    return ""


def is_accessible( field: Field[ int ] ) -> bool:
    end_point = (field.width - 2, field.height - 2)
    way_field = field_value( field.width, field.height, False )
    wave = [ (1, 1, 1) ]
    while wave:
        pt = wave.pop()
        if pt == end_point: return True
        if field[ pt ] == OBSTACLE or way_field[ pt ]: continue
        way_field[ pt ] = True
        for d in CROSS_DIRS: wave.append( (pt[ 0 ] + d[ 0 ], pt[ 1 ] + d[ 1 ]) )
    pass


def main():
    exec_tasks(
        functools.partial( prepare, dim = 7, drops_count = 12 ),
        task1,
        task2,
        read_file( 'data/day24_18.sample' ),
        22,
        "6,1"
    )
    exec_tasks(
        functools.partial( prepare, dim = 71, drops_count = 1024 ),
        task1,
        task2,
        read_file( 'data/day24_18.in' ),
        320,
        "34,40"
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
