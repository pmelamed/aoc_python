import itertools
import re
from typing import Literal, Optional

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


class Data:
    flows: dict[ str, int ]
    distances: dict[ DistanceKey, int ]
    bits: dict[ str, int ]

    def __init__( self, flows: dict[ str, int ], distances: dict[ DistanceKey, int ], bits: dict[ str, int ] ) -> None:
        self.flows = flows
        self.distances = distances
        self.bits = bits


class CharPos:
    room: str
    time_left: int

    def __init__( self, room: str, time_left: int, way: str ) -> None:
        self.room = room
        self.time_left = time_left
        self.way = way


class State:
    characters: tuple[ CharPos, CharPos ]
    closed: set[ str ]
    agg_flow: int
    way: str

    def __init__( self, characters: tuple[ CharPos, CharPos ], closed: set[ str ], agg_flow: int ):
        self.characters = characters
        self.closed = closed
        self.agg_flow = agg_flow


def parse_data( lines: list[ str ] ) -> Data:
    rooms: list[ Room ] = [ ]
    for line in lines:
        match = INPUT_PATTERN.match( line )
        rooms.append( Room( match.group( 1 ), int( match.group( 2 ) ), match.group( 3 ).split( ", " ) ) )
    flows = dict( (room.name, room.flow) for room in rooms if room.flow > 0 )
    bits = dict( [ (name, 1 << bit) for bit, name in enumerate( flows.keys() ) ] )

    distances: dict[ DistanceKey, int ] = dict(
            [
                *itertools.chain.from_iterable(
                        [ [ ((room.name, dst), 1) for dst in room.tunnels ] for room in rooms ]
                )
            ]
    )
    distances.update( dict( ((room.name, room.name), 0) for room in rooms ) )
    wave: set[ str ] = set( flows.keys() )
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
            and (item[ 0 ][ 0 ] == "AA" or item[ 0 ][ 0 ] in flows)
            and item[ 0 ][ 1 ] in flows
    )
    return Data( flows, distances, bits )


def task1( data: Data ) -> int:
    return find_way(
            "AA",
            set( data.flows.keys() ),
            data.distances,
            data.flows,
            TASK1_MINUTES,
            0,
            "AA"
    )


def task2( data: Data ) -> int:
    print( f"Rooms with flow[{len( data.flows )}] = {data.flows}" )
    return 0
    # return find_way2(
    #         State(
    #                 (CharPos( "AA", TASK2_MINUTES, "AA" ), CharPos( "AA", TASK2_MINUTES, "AA" )),
    #                 { *data.flows.keys() },
    #                 0
    #         ),
    #         data.distances,
    #         data.flows
    # )


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
        new_closed = closed - { target }
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


def get_updated_state(
        state: State,
        character: Literal[ 0, 1 ],
        target: str,
        distances: dict[ DistanceKey, int ],
        flows: dict[ str, int ]
) -> Optional[ State ]:
    chars: tuple[ CharPos, CharPos ] = state.characters
    char_pos = chars[ character ]
    pos = char_pos.room
    time_left = char_pos.time_left
    distance = distances[ (pos, target) ]
    if time_left < distance + 1:
        return None
    new_pos = CharPos(
            target,
            time_left - distance - 1,
            f"{char_pos.way} --{distance}--> {target}(t={time_left - distance - 1},dF={flows[ target ]})"
    )
    chars = (new_pos, chars[ 1 ]) if character == 0 else (chars[ 0 ], new_pos)
    return State(
            chars,
            state.closed - { target },
            state.agg_flow + chars[ character ].time_left * flows[ target ]
    )


def find_way2( state: Optional[ State ], distances: dict[ DistanceKey, int ], flows: dict[ str, int ] ) -> int:
    if state is None:
        return 0
    max_flow = state.agg_flow
    for target in state.closed:
        max_flow = max(
                max_flow,
                find_way2( get_updated_state( state, 0, target, distances, flows ), distances, flows ),
                find_way2( get_updated_state( state, 1, target, distances, flows ), distances, flows )
        )
        # if max_flow == state.agg_flow:
        #     print( f"\n{state.agg_flow} vvv" )
        #     for cp in state.characters:
        #         print( f"    {cp.way}" )
    return max_flow


def enum_best_ways(
        data: Data,
        best_ways: dict[ int, int ],
        current_pos: str,
        minutes_left: int,
        agg_flow: int,
        current_mask: int,
        closed: set[ str ]
) -> None:
    best_ways[ current_mask ] = max( best_ways[ current_mask ], agg_flow ) if current_mask in best_ways else agg_flow
    if minutes_left == 0 or len( closed ) == 0:
        return
    targets = dict(
            (key[ 1 ], distance) for key, distance in data.distances.items()
            if key[ 0 ] == current_pos and key[ 1 ] in closed
    )
    for target, distance in targets.items():
        if distance + 1 > minutes_left:
            continue
        new_minutes_left = minutes_left - distance - 1
        new_agg_flow = agg_flow + new_minutes_left * flows[ target ]
        new_closed = closed - { target }
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

    pass


def main():
    helper.verbose_level = 0
    helper.exec_tasks(
            parse_data,
            task1,
            task2,
            read_file( '../data/input/year22/day22_16.in' ),
            1862,
            None
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
