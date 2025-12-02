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


class Data:
    boxes: Boxes
    supports: list[ set[ int ] ] = list()
    supported: list[ set[ int ] ] = list()

    def __init__( self, lines: list[ str ] ):
        boxes = sorted( [ parse_box( line ) for line in lines ], key = lambda b: b.a.z )
        supports: list[ set[ int ] ] = list()
        supported: list[ set[ int ] ] = list()
        width = max( box.b.x for box in boxes ) + 1
        height = max( box.b.y for box in boxes ) + 1
        top_view: helper.Field[ CellInfo ] = field_value( width, height, CellInfo( box = -1, height = 0 ) )
        for index, box in enumerate( boxes ):
            max_height = max(
                    top_view[ cell ].height
                    for cell in product(
                        range( box.a.x, box.b.x + 1 ),
                        range( box.a.y, box.b.y + 1 )
                        )
                    )
            new_height = max_height + box.b.z - box.a.z + 1
            supports.append( set() )
            supported.append( set() )
            for cell_coords in product( range( box.a.x, box.b.x + 1 ), range( box.a.y, box.b.y + 1 ) ):
                cell = top_view[ cell_coords ]
                if cell.height == max_height and cell.box >= 0:
                    supports[ cell.box ].add( index )
                    supported[ index ].add( cell.box )
                top_view[ cell_coords ] = CellInfo( box = index, height = new_height )
        self.boxes = boxes
        self.supports = supports
        self.supported = supported


def task1( data: Data ) -> int:
    return sum(
            1 for box_index in range( len( data.boxes ) ) if
            all_supported( data.supports[ box_index ], data.supported )
            )


def task2( data: Data ) -> int:
    result = 0
    for box_index in range( len( data.boxes ) ):
        fallen: set[ int ] = { box_index }
        for supported_index in range( box_index + 1, len( data.boxes ) ):
            if (len( data.supported[ supported_index ] & fallen ) != 0
                    and len( data.supported[ supported_index ] - fallen ) == 0):
                fallen.add( supported_index )
        result += len( fallen ) - 1
    return result


def parse_box( line: str ) -> Rect3D:
    return Rect3D.from_coords_list(
        map( int, re.findall( RE_BOX, line )[ 0 ] ),
        sort = True
        )


def all_supported( supported_boxes: Iterable[ int ], supported_by: list[ set[ int ] ] ) -> bool:
    return all( len( supported_by[ box_index ] ) > 1 for box_index in supported_boxes )


def main():
    helper.exec_tasks(
        Data,
        task1,
        task2,
        helper.read_file( 'data/day23_22.sample' ),
        5,
        7
        )
    helper.exec_tasks(
        Data,
        task1,
        task2,
        helper.read_file( 'data/day23_22.in' ),
        389,
        70609
        )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        helper.print_ex( ex )
