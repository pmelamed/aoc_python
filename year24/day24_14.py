import re
from collections import defaultdict
from functools import partial, reduce

from PIL import Image, ImageDraw

from helper import Coord, Direction, exec_task, exec_tasks, print_ex, read_file


type RobotData = tuple[ Coord, Direction ]
type Data = list[ RobotData ]


def prepare( lines: list[ str ] ) -> Data:
    return [ parse_line( line ) for line in lines ]


def task1( width: int, height: int, data: Data ) -> int:
    quadrants = [ 0, 0, 0, 0, 0 ]
    half_width = width // 2
    half_height = height // 2
    for robot in data:
        quadrants[ get_quadrant( move_robot( robot, width, height, 100 ), half_width, half_height ) ] += 1
    return reduce( lambda a, b: a * b, quadrants[ 1: ], 1 )


def task2( width: int, height: int, data: Data ) -> int:
    pts = [ robot[ 0 ] for robot in data ]
    counts = defaultdict( lambda: 0 )
    step = 0
    for _ in range( 1, 100000 ):
        counts.clear()
        step += 1
        for index in range( len( data ) ):
            pts[ index ] = (
                (pts[ index ][ 0 ] + data[ index ][ 1 ][ 0 ] + width) % width,
                (pts[ index ][ 1 ] + data[ index ][ 1 ][ 1 ] + height) % height
            )
            counts[ pts[ index ] ] += 1
        if max( counts.values() ) == 1:
            img = Image.new( "1", (width, height) )
            draw = ImageDraw.Draw( img )
            draw.point( pts, 1 )
            img.save( f"../data/output/day14-{str( step ).rjust( 6, "0" )}.png" )
            return step
    return 0


def parse_line( line: str ) -> RobotData:
    x, y, dx, dy = re.findall( r"^p=([0-9]+),([0-9]+) v=(-?[0-9]+),(-?[0-9]+)$", line )[ 0 ]
    return (int( x ), int( y )), (int( dx ), int( dy ))


def move_robot( robot: RobotData, width: int, height: int, time: int ) -> Coord:
    (x, y), (dx, dy) = robot
    x = (x + dx * time) % width
    if x < 0:
        x += width
    y = (y + dy * time) % height
    if y < 0:
        y += height
    return x, y


def get_quadrant( pt: Coord, half_width: int, half_height: int ):
    if pt[ 0 ] == half_width or pt[ 1 ] == half_height:
        return 0
    return pt[ 0 ] // (half_width + 1) * 2 + pt[ 1 ] // (half_height + 1) + 1


def main():
    exec_task( prepare, partial( task1, 11, 7 ), read_file( '../data/samples/year24/day24_14.sample' ), 12 )
    exec_tasks(
        prepare,
        partial( task1, 101, 103 ),
        partial( task2, 101, 103 ),
        read_file( '../data/input/year24/day24_14.in' ),
        214400550,
        8149
        )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
