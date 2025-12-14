import collections
import itertools

import helper


class Data:
    rect: helper.Rect
    antenna: dict[ int, list[ helper.Coord ] ]

    def __init__(
            self,
            rect: helper.Rect,
            antenna: dict[ int, list[ helper.Coord ] ]
            ):
        self.rect = rect
        self.antenna = antenna


def prepare( lines: list[ str ] ) -> Data:
    antenna = collections.defaultdict( list )
    height = 0
    width = 0
    for y, symbols in enumerate( bytes( line, "UTF-8" ) for line in lines ):
        height += 1
        width = len( symbols )
        for x, symbol in enumerate( symbols ):
            if symbol != ord( '.' ):
                antenna[ symbol ].append( (x, y) )
    return Data( helper.field_rect( width, height ), antenna )


def task1( data: Data ) -> int:
    antinodes: set[ helper.Coord ] = set()
    for antennas in data.antenna.values():
        for a1, a2 in itertools.combinations( antennas, 2 ):
            d = helper.coord_sub( a2, a1 )
            [ antinodes.add( node )
              for node in (helper.coord_sub( a1, d ), helper.coord_add( a2, d ))
              if helper.inside_rect( node, data.rect ) ]
    return len( antinodes )


def task2( data: Data ) -> int:
    antinodes: set[ helper.Coord ] = set()
    for antennas in data.antenna.values():
        for a1, a2 in itertools.combinations( antennas, 2 ):
            pair_nodes: list[ helper.Coord ] = [ a1, a2 ]
            d = helper.coord_sub( a2, a1 )

            node = helper.coord_sub( a1, d )
            while helper.inside_rect( node, data.rect ):
                pair_nodes.append( node )
                node = helper.coord_sub( node, d )

            node = helper.coord_add( a2, d )
            while helper.inside_rect( node, data.rect ):
                pair_nodes.append( node )
                node = helper.coord_add( node, d )
            antinodes.update( pair_nodes )
    return len( antinodes )


def main():
    helper.exec_tasks( prepare, task1, task2, helper.read_file( '../data/samples/year24/day24_08.sample' ), 14, 34 )
    helper.exec_tasks( prepare, task1, task2, helper.read_file( '../data/input/year24/day24_08.in' ), 409, 1308 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        helper.print_ex( ex )
