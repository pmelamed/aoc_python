from itertools import count

import helper
from geom2d import Coord2D, CROSS_DIRS_2D, Field2D
from helper import SYM_OBSTACLE, SYM_PLANE, SYM_START

TASK2_STEPS = 26501365


class Data:
    field: Field2D[ int ]
    start_pt: Coord2D

    def __init__( self,
                  lines: list[ str ] ):
        self.field = Field2D.from_input( lines )
        self.start_pt = self.field.find( lambda _x, _y, cell: cell == SYM_START )
        self.field[ self.start_pt ] = SYM_PLANE


def task1( data: Data ) -> int:
    visited: Field2D[ bool ] = Field2D.from_value( data.field.width, data.field.height, False )
    visited[ data.start_pt ] = True
    step: set[ Coord2D ] = { data.start_pt }
    for _ in range( 64 ):
        next_step = [ ]
        for pts in ((npt
                     for npt in (p + d for d in CROSS_DIRS_2D)
                     if npt in data.field and data.field[ npt ] != SYM_OBSTACLE)
                    for p in step):
            next_step.extend( pts )
            pass
        step.clear()
        step.update( next_step )
        for pt in step: visited[ pt ] = True
    return len( step )


def task2( data: Data ) -> int:
    return 0


def main():
    helper.exec_tasks( Data,
                       task1,
                       task2,
                       helper.read_file( 'data/day23_21.in' ),
                       3542,
                       None )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        helper.print_ex( ex )
