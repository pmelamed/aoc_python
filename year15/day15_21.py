import itertools
from typing import Iterable

from helper import exec_tasks, print_ex, read_file


class Equipment:
    cost: int
    damage: int
    armor: int

    def __init__( self, cost: int, damage: int, armor: int ):
        self.cost = cost
        self.damage = damage
        self.armor = armor


class Player:
    hit_points: int
    damage: int
    armor: int

    def __init__( self, hit_points: int, damage: int, armor: int ):
        self.hit_points = hit_points
        self.damage = damage
        self.armor = armor


MISSING_EQUIPMENT = Equipment( 0, 0, 0 )

WEAPONS = [
    Equipment( 8, 4, 0 ),
    Equipment( 10, 5, 0 ),
    Equipment( 25, 6, 0 ),
    Equipment( 40, 7, 0 ),
    Equipment( 75, 8, 0 )
]

ARMOR = [
    MISSING_EQUIPMENT,
    Equipment( 13, 0, 1 ),
    Equipment( 31, 0, 2 ),
    Equipment( 53, 0, 3 ),
    Equipment( 75, 0, 4 ),
    Equipment( 102, 0, 5 )
]

RINGS = [
    MISSING_EQUIPMENT,
    Equipment( 25, 1, 0 ),
    Equipment( 50, 2, 0 ),
    Equipment( 100, 3, 0 ),
    Equipment( 20, 0, 1 ),
    Equipment( 40, 0, 2 ),
    Equipment( 80, 0, 3 )
]


def parse_data( lines: list[ str ] ) -> Player:
    return Player(
            int( lines[ 0 ].split( ": " )[ 1 ] ),
            int( lines[ 1 ].split( ": " )[ 1 ] ),
            int( lines[ 2 ].split( ": " )[ 1 ] )
    )


def task1( data: Player ) -> int:
    min_cost = 1000
    for equipment in itertools.product( WEAPONS, ARMOR, RINGS, RINGS ):
        if equipment[2] == equipment[3]:
            continue
        cost = sum( e.cost for e in equipment )
        if cost >= min_cost:
            continue
        if battle( 100, equipment, data ):
            min_cost = cost
    return min_cost


def task2( data: Player ) -> int:
    max_cost = 0
    for equipment in itertools.product( WEAPONS, ARMOR, RINGS, RINGS ):
        if equipment[2] == equipment[3]:
            continue
        cost = sum( e.cost for e in equipment )
        if cost <= max_cost:
            continue
        if not battle( 100, equipment, data ):
            max_cost = cost
    return max_cost


def single_hit( attacker_damage: int, defender_armor: int ) -> int:
    return max( attacker_damage - defender_armor, 1 )


def battle( hit_points: int, equipment: Iterable[ Equipment ], boss: Player ) -> bool:
    hp_me = hit_points
    hp_boss = boss.hit_points
    damage = sum( e.damage for e in equipment )
    armor = sum( e.armor for e in equipment )
    while True:
        hit = single_hit( damage, boss.armor )
        hp_boss -= hit
        if hp_boss <= 0:
            return True
        hit = single_hit( boss.damage, armor )
        hp_me -= hit
        if hp_me <= 0:
            return False


def main():
    exec_tasks(
            parse_data,
            task1,
            task2,
            read_file( '../data/input/year15/day15_21.in' ),
            111,
            188
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
