import functools

from geom2d import Coord2D, Field2D, SYM_DIRS_2D
from helper import exec_tasks, print_ex, read_file, SYM_DIRS, SYM_OBSTACLE

START_POINT = Coord2D.from_coords( 1, 0 )


class Data:
    field: Field2D[ int ]

    def __init__( self, lines: list[ str ] ):
        self.field = Field2D.from_input( lines )


def task1( data: Data ) -> int:
    return find_longest_way( data.field, True )


def task2( data: Data ) -> int:
    return find_longest_way( data.field, False )


def find_longest_way( field: Field2D[ int ], respect_slopes: bool ) -> int:
    longest = 0
    target_graph, end_point_index = get_crosses_graph( field, respect_slopes )
    path: list[ tuple[ int, int ] ] = [ (0, 0) ]
    visited: set[ int ] = { 0 }
    while path:
        pt, length = path.pop()
        if length == -1:
            visited.discard( pt )
            continue
        if pt == end_point_index:
            longest = max( longest, length )
            continue
        visited.add( pt )
        path.append( (pt, -1) )
        path.extend( [ (p, length + l) for p, l in target_graph[ pt ].items() if p not in visited ] )
    return longest


def get_crosses_graph( field, respect_slopes ):
    end_point = get_end_point( field )
    neighbors = generate_neighbours( field, respect_slopes )
    crosses: list[ Coord2D ] = [ Coord2D( x, y ) for x, y in neighbors.range()
                                 if len( neighbors[ Coord2D( x, y ) ] ) > 2 ]
    crosses.insert( 0, START_POINT )
    crosses.append( end_point )
    end_point_index = len( crosses ) - 1
    crosses_map: dict[ Coord2D, int ] = dict( (coord, index) for index, coord in enumerate( crosses ) )
    target_graph: dict[ int, dict[ int, int ] ] = dict()
    for index in range( end_point_index ):
        target_graph[ index ] = dict( (crosses_map[ coord ], length)
                                      for coord, length in find_nearest_crosses( field,
                                                                                 neighbors,
                                                                                 crosses[ index ] ) )
    return target_graph, end_point_index


def get_end_point( field: Field2D[ int ] ):
    return Coord2D( field.width - 2, field.height - 1 )


def find_nearest_crosses( field: Field2D[ int ],
                          neighbors: Field2D[ list[ Coord2D ] ],
                          start_pt: Coord2D ) -> list[ tuple[ Coord2D, int ] ]:
    result: list[ tuple[ Coord2D, int ] ] = [ ]
    end_point = get_end_point( field )
    path: list[ tuple[ Coord2D, int ] ] = [ (pt, 0) for pt in neighbors[ start_pt ] ]
    visited: Field2D[ bool ] = Field2D.from_value( field.width, field.height, False )
    visited[ start_pt ] = True
    while path:
        pt, length = path.pop()
        if length == -1:
            visited[ pt ] = False
            continue
        if pt == START_POINT: continue
        if len( neighbors[ pt ] ) > 2 or pt == end_point:
            result.append( (pt, length + 1) )
            continue
        visited[ pt ] = True
        path.append( (pt, -1) )
        path.extend( [ (p, length + 1) for p in neighbors[ pt ] if not visited[ p ] ] )
    return result


def generate_neighbours( field: Field2D[ int ], respect_slopes: bool ) -> Field2D[ list[ Coord2D ] ]:
    return Field2D.from_generate( field.width,
                                  field.height,
                                  functools.partial( get_cell_neighbors,
                                                     field = field,
                                                     respect_slopes = respect_slopes ) )


def get_cell_neighbors( pt: Coord2D, field: Field2D[ int ], respect_slopes: bool ) -> list[ Coord2D ]:
    cell = field[ pt ]
    if cell == SYM_OBSTACLE: return [ ]
    candidates = ([ pt + SYM_DIRS_2D[ cell ] ]
                  if respect_slopes and cell in SYM_DIRS
                  else [ pt + d for d in SYM_DIRS_2D.values() ])
    return [ p for p in candidates if p in field and field[ p ] != SYM_OBSTACLE ]


def main():
    exec_tasks( Data,
                task1,
                task2,
                read_file( 'data/day23_23.sample' ),
                94,
                154 )
    exec_tasks( Data,
                task1,
                task2,
                read_file( 'data/day23_23.in' ),
                2050,
                6262 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
