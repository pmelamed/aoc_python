import functools
import operator
import re
from typing import Callable


import helper
from helper import exec_tasks, print_ex, read_file


def parse_data( lines: list[ str ] ) -> list[ int ]:
    return [ int( line ) for line in lines ]


def task1( data: list[ int ] ) -> int:
    group_weight = sum( data ) // 3
    full_set = set( data )
    sorted_data = sorted( data, reverse = True )
    min_group_size = 0
    subtotal = 0
    while subtotal < group_weight:
        subtotal += sorted_data[ min_group_size ]
        min_group_size += 1
    for group1_size in range( min_group_size, len( data ) ):
        store = [ ]
        combinations_generator( sorted_data, 0, group1_size * [ 0 ], 0, group_weight, 0, store )
        store = sorted( store, key = lambda lst: functools.reduce( operator.mul, lst ) )
        for group1_content in store:
            if can_make_weight( list( full_set - group1_content ), 0, group_weight ):
                return functools.reduce( operator.mul, group1_content )
    return 0


def task2( data: list[ int ] ) -> int:
    group_weight = sum( data ) // 4
    full_set = set( data )
    sorted_data = sorted( data, reverse = True )
    min_group_size = 0
    subtotal = 0
    while subtotal < group_weight:
        subtotal += sorted_data[ min_group_size ]
        min_group_size += 1
    for group1_size in range( min_group_size, len( data ) ):
        store = [ ]
        combinations_generator( sorted_data, 0, group1_size * [ 0 ], 0, group_weight, 0, store )
        store = sorted( store, key = lambda lst: functools.reduce( operator.mul, lst ) )
        for group1_content in store:
            if make_weight(
                    list( full_set - group1_content ),
                    0,
                    [ ],
                    group_weight,
                    0,
                    lambda rest: can_make_weight( list( rest ), 0, group_weight )
            ):
                return functools.reduce( operator.mul, group1_content )
    return 0


def combinations_generator(
        data: list[ int ],
        data_start_idx: int,
        used: list[ int ],
        used_idx: int,
        target_total: int,
        subtotal: int,
        store: list[ set[ int ] ]
):
    if used_idx == len( used ):
        if subtotal == target_total:
            used_set = set( used )
            store.append( used_set )
            if sum( used_set ) != target_total:
                print( f"{used} -> {used_set} != {target_total}" )
                assert False
        return
    for idx in range( data_start_idx, len( data ) ):
        new_subtotal = subtotal + data[ idx ]
        if new_subtotal > target_total:
            continue
        used[ used_idx ] = data[ idx ]
        combinations_generator(
                data,
                idx + 1,
                used,
                used_idx + 1,
                target_total,
                new_subtotal,
                store
        )


def can_make_weight( weights: list[ int ], start_idx: int, target_weight: int ) -> bool:
    for idx in range( start_idx, len( weights ) ):
        weight = weights[ idx ]
        if target_weight == weight or can_make_weight( weights, idx + 1, target_weight - weight ):
            return True
    return False


def make_weight(
        weights: list[ int ],
        start_idx: int,
        used: list[ int ],
        target_total: int,
        subtotal: int,
        callback: Callable[ [ set[ int ] ], bool ]
) -> bool:
    if subtotal == target_total:
        return callback( set( weights ) - set( used ) )
    for idx in range( start_idx, len( weights ) ):
        weight = weights[ idx ]
        new_subtotal = subtotal + weight
        if new_subtotal > target_total:
            continue
        used.append( weight )
        if make_weight( weights, idx + 1, used, target_total, new_subtotal, callback ):
            return True
        used.pop()
    return False


def main():
    helper.verbose_level = 0
    exec_tasks(
            parse_data,
            task1,
            task2,
            read_file( '../data/input/year15/day15_24.in' ),
            11846773891,
            80393059
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
