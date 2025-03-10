import helper
from geom2d import Coord2D, DIR_DOWN, SYM_DIRS_2D, SYM_DOWN, SYM_LEFT, SYM_RIGHT
from helper import SYM_OBSTACLE, SYM_PLANE


class Figure:
    image: list[ str ]
    blocks: list[ Coord2D ]
    edges: dict[ int, list[ Coord2D ] ]
    height: int

    def __init__( self,
                  height: int,
                  blocks: list[ Coord2D ],
                  edges: dict[ int, list[ Coord2D ] ] ):
        self.height = height
        self.blocks = blocks
        self.edges = edges


FIGURES: list[ Figure ] = [
    Figure(
        1,
        [ Coord2D( 0, 0 ), Coord2D( 1, 0 ), Coord2D( 2, 0 ), Coord2D( 3, 0 ) ],
        {
            SYM_DOWN:  [ Coord2D( 0, 1 ), Coord2D( 1, 1 ), Coord2D( 2, 1 ), Coord2D( 3, 1 ) ],
            SYM_LEFT:  [ Coord2D( -1, 0 ) ],
            SYM_RIGHT: [ Coord2D( 4, 0 ) ]
        }
    ),
    Figure(
        3,
        [ Coord2D( 1, 0 ), Coord2D( 0, 1 ), Coord2D( 1, 1 ), Coord2D( 2, 1 ), Coord2D( 1, 2 ) ],
        {
            SYM_DOWN:  [ Coord2D( 0, 2 ), Coord2D( 1, 3 ), Coord2D( 2, 2 ) ],
            SYM_LEFT:  [ Coord2D( 0, 0 ), Coord2D( -1, 1 ), Coord2D( 0, 2 ) ],
            SYM_RIGHT: [ Coord2D( 2, 0 ), Coord2D( 3, 1 ), Coord2D( 2, 2 ) ]
        }
    ),
    Figure(
        3,
        [ Coord2D( 2, 0 ), Coord2D( 2, 1 ), Coord2D( 0, 2 ), Coord2D( 1, 2 ), Coord2D( 2, 2 ) ],
        {
            SYM_DOWN:  [ Coord2D( 0, 3 ), Coord2D( 1, 3 ), Coord2D( 2, 3 ) ],
            SYM_LEFT:  [ Coord2D( 1, 0 ), Coord2D( 1, 1 ), Coord2D( -1, 2 ) ],
            SYM_RIGHT: [ Coord2D( 3, 0 ), Coord2D( 3, 1 ), Coord2D( 3, 2 ) ]
        }
    ),
    Figure(
        4,
        [ Coord2D( 0, 0 ), Coord2D( 0, 1 ), Coord2D( 0, 2 ), Coord2D( 0, 3 ) ],
        {
            SYM_DOWN:  [ Coord2D( 0, 4 ) ],
            SYM_LEFT:  [ Coord2D( -1, 0 ), Coord2D( -1, 1 ), Coord2D( -1, 2 ), Coord2D( -1, 3 ) ],
            SYM_RIGHT: [ Coord2D( 1, 0 ), Coord2D( 1, 1 ), Coord2D( 1, 2 ), Coord2D( 1, 3 ) ]
        }
    ),
    Figure(
        2,
        [ Coord2D( 0, 0 ), Coord2D( 1, 0 ), Coord2D( 0, 1 ), Coord2D( 1, 1 ) ],
        {
            SYM_DOWN:  [ Coord2D( 0, 2 ), Coord2D( 1, 2 ) ],
            SYM_LEFT:  [ Coord2D( -1, 0 ), Coord2D( -1, 1 ) ],
            SYM_RIGHT: [ Coord2D( 2, 0 ), Coord2D( 2, 1 ) ]
        }
    )
]

EMPTY_CHAMBER_LINE = [ SYM_PLANE for _ in range( 7 ) ]


class SymData:
    steam_jets: str
    steam_jet_ptr: int
    chamber: list[ list[ int ] ]

    def __init__( self, steams: str ):
        self.steam_jets = steams
        self.steam_jet_ptr = -1
        self.chamber = [ ]

    def next_steam_jet( self ) -> int:
        self.steam_jet_ptr = (self.steam_jet_ptr + 1) % len( self.steam_jets )
        return ord( self.steam_jets[ self.steam_jet_ptr ] )

    def print_chamber( self ):
        for line in self.chamber:
            print( "".join( [ *map( chr, line ) ] ) )
        print()


def task1( steam_jets: str ) -> int:
    sym_data = SymData( steam_jets )
    for figure_idx in range( 2022 ):
        sym_figure( sym_data, FIGURES[ figure_idx % len( FIGURES ) ] )
        # sym_data.print_chamber()
    return len( sym_data.chamber )


def task2( steam_jets: str ) -> int:

    return 0


def sym_figure( sym_data: SymData, figure: Figure ):
    fpos = Coord2D( 2, -3 - figure.height )
    # Move
    moved = True
    while moved:
        steam_jet = sym_data.next_steam_jet()
        if can_move( sym_data, figure, fpos, steam_jet ): fpos += SYM_DIRS_2D[ steam_jet ]
        moved = can_move( sym_data, figure, fpos, SYM_DOWN )
        if moved:
            fpos += DIR_DOWN

    # Plot
    #  Extend chamber up if needed
    # print( "Movement ended at {}", fpos )
    while fpos.y < 0:
        sym_data.chamber.insert( 0, EMPTY_CHAMBER_LINE.copy() )
        fpos += DIR_DOWN
    for pt in (pt + fpos for pt in figure.blocks):
        sym_data.chamber[ pt.y ][ pt.x ] = SYM_OBSTACLE
    return


def can_move( sym_data: SymData, figure: Figure, fpos: Coord2D, steam_jet: int ) -> bool:
    return not any( pt.x < 0 or pt.x >= 7
                    or pt.y >= len( sym_data.chamber )
                    or (pt.y >= 0 and sym_data.chamber[ pt.y ][ pt.x ] != SYM_PLANE)
                    for pt in (pt + fpos for pt in figure.edges[ steam_jet ]) )


def main():
    helper.exec_tasks( None,
                       task1,
                       task2,
                       helper.read_file( 'data/day22_17.sample' )[ 0 ],
                       3068,
                       1_514_285_714_288 )
    helper.exec_tasks( None,
                       task1,
                       task2,
                       helper.read_file( 'data/day22_17.in' )[ 0 ],
                       3147,
                       None )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        helper.print_ex( ex )
