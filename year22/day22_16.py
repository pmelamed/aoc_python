import itertools
import re

import helper
from helper import print_ex, read_file


INPUT_PATTERN = re.compile( r"^Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z ,]+)$" )
TASK1_MINUTES = 30
TASK2_MINUTES = 26


class Room:
    name: str
    flow: int
    tunnels: list[ str ]

    def __init__( self, name: str, flow: int, tunnels: list[ str ] ) -> None:
        self.name = name
        self.flow = flow
        self.tunnels = tunnels

    def __str__( self ) -> str:
        return f"Room {self.name}, flow={self.flow}, doors={self.tunnels}"


type DistanceKey = tuple[ str, str ]


def parse_data( lines: list[ str ] ) -> list[ Room ]:
    result: list[ Room ] = [ ]
    for line in lines:
        match = INPUT_PATTERN.match( line )
        tunnel = Room( match.group( 1 ), int( match.group( 2 ) ), match.group( 3 ).split( ", " ) )
        result.append( tunnel )
    return result


def task1( data: list[ Room ] ) -> int:
    result = 0
    distances: dict[ DistanceKey, int ] = dict(
            [
                *itertools.chain.from_iterable(
                        [ [ ((room.name, dst), 1) for dst in room.tunnels ] for room in data ]
                )
            ]
    )
    distances.update( dict( ((room.name, room.name), 0) for room in data ) )
    rooms_with_flow = set( room.name for room in data if room.flow > 0 )
    wave: set[ str ] = set( rooms_with_flow )
    while wave:
        room = wave.pop()
        all_src = [ (key[ 0 ], distance) for (key, distance) in distances.items() if key[ 1 ] == room ]
        all_dst = [ (key[ 1 ], distance) for (key, distance) in distances.items() if key[ 0 ] == room ]
        for src_room in all_src:
            src_room_name = src_room[ 0 ]
            src_room_dist = src_room[ 1 ]
            for dst_room in all_dst:
                dst_room_name = dst_room[ 0 ]
                dst_room_dist = dst_room[ 1 ]
                new_dist = src_room_dist + dst_room_dist
                distance_key = (src_room_name, dst_room_name)
                if not distance_key in distances or new_dist < distances[ distance_key ]:
                    distances[ distance_key ] = new_dist
                    wave.add( dst_room_name )
    distances = dict(
            item for item in distances.items()
            if item[ 1 ] != 0
            and (item[ 0 ][ 0 ] == "AA" or item[ 0 ][ 0 ] in rooms_with_flow)
            and item[ 0 ][ 1 ] in rooms_with_flow

    )
    flows = dict( (room.name, room.flow) for room in data if room.flow > 0 )
    return find_way(
            "AA",
            set( rooms_with_flow ),
            distances,
            flows,
            TASK1_MINUTES,
            0,
            "AA"
    )


def find_way(
        pos: str,
        closed: set[ str ],
        distances: dict[ DistanceKey, int ],
        flows: dict[ str, int ],
        minutes_left: int,
        agg_flow: int,
        current_way: str
) -> int:
    if minutes_left == 0 or len( closed ) == 0:
        # print( f"{current_way} ==> {agg_flow}" )
        return agg_flow
    targets = dict(
            (key[ 1 ], distance) for key, distance in distances.items()
            if key[ 0 ] == pos and key[ 1 ] in closed
    )
    max_flow = agg_flow
    for target, distance in targets.items():
        if distance + 1 > minutes_left:
            continue
        new_minutes_left = minutes_left - distance - 1
        new_agg_flow = agg_flow + new_minutes_left * flows[ target ]
        new_closed = closed.copy()
        new_closed.remove( target )
        new_flow = find_way(
                target,
                new_closed,
                distances,
                flows,
                new_minutes_left,
                new_agg_flow,
                f"{current_way} --{distance}--> {target}(dF={flows[ target ]},F={new_agg_flow},t={new_minutes_left})"
        )
        if new_flow > max_flow:
            max_flow = new_flow
    return max_flow


def main():
    helper.verbose_level = 0
    helper.exec_task(
            parse_data,
            task1,
            read_file( '../data/input/year22/day22_16.in' ),
            1862
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
