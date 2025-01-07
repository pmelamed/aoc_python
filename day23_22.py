import re
from collections import namedtuple
from itertools import product
from typing import Iterable

import helper
from geom3d import Rect3D
from helper import field_value

RE_BOX = r"([0-9]+),([0-9]+),([0-9]+)~([0-9]+),([0-9]+),([0-9]+)"

type Boxes = list[ Rect3D ]
CellInfo = namedtuple( "CellInfo", [ "box", "height" ] )


def prepare( lines: list[ str ] ) -> Boxes:
    result = sorted( [ parse_box( line ) for line in lines ], key = lambda b: b.a.z )
    return result


def task1( boxes: Boxes ) -> int:
    supports: list[ set[ int ] ] = list()
    supported: list[ set[ int ] ] = list()
    width = max( box.b.x for box in boxes ) + 1
    height = max( box.b.y for box in boxes ) + 1
    top_view: helper.Field[ CellInfo ] = field_value( width, height, CellInfo( box = -1, height = 0 ) )
    for index, box in enumerate( boxes ):
        max_height = max( top_view[ cell ].height
                          for cell in product( range( box.a.x, box.b.x + 1 ),
                                               range( box.a.y, box.b.y + 1 ) ) )
        # print( f"{chr( ord( 'A' ) + index )} = {box}" )
        # print( top_view.dump( lambda _x, _y, cell: f"[{chr( ord( 'A' ) + cell.box )},{cell.height:3}]" ) )
        new_height = max_height + box.b.z - box.a.z + 1
        supports.append( set() )
        supported.append( set() )
        for cell_coords in product( range( box.a.x, box.b.x + 1 ), range( box.a.y, box.b.y + 1 ) ):
            cell = top_view[ cell_coords ]
            if cell.height == max_height and cell.box >= 0:
                supports[ cell.box ].add( index )
                supported[ index ].add( cell.box )
            top_view[ cell_coords ] = CellInfo( box = index, height = new_height )
    # for box_index in range( len( boxes ) ):
    #     print( f"Box {chr( ord( 'A' ) + box_index )}" )
    #     print( f"  Supports {[ chr( ord( 'A' ) + i ) for i in supports[ box_index ] ]}" )
    #     print( f"  Supported by {[ chr( ord( 'A' ) + i ) for i in supported[ box_index ] ]}" )
    disintegratable = [ box_index for box_index in range( len( boxes ) ) if
                        all_supported( supports[ box_index ], supported ) ]
    # print( [ chr( ord( 'A' ) + i ) for i in disintegratable ] )
    return len( disintegratable )


def task2( boxes: Boxes ) -> int:
    return 0


def parse_box( line: str ) -> Rect3D:
    return Rect3D.from_coords_list( map( int, re.findall( RE_BOX, line )[ 0 ] ),
                                    sort = True )


def all_supported( supported_boxes: Iterable[ int ], supported_by: list[ set[ int ] ] ) -> bool:
    return all( len( supported_by[ box_index ] ) > 1 for box_index in supported_boxes )


def main():
    helper.exec_tasks( prepare,
                       task1,
                       task2,
                       helper.read_file( 'data/day23_22.sample' ),
                       5,
                       None )
    helper.exec_tasks( prepare,
                       task1,
                       task2,
                       helper.read_file( 'data/day23_22.in' ),
                       None,
                       None )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        helper.print_ex( ex )
