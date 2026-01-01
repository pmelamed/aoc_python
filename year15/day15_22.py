from typing import Callable

import helper
from helper import exec_tasks, print_ex, read_file


INITIAL_MANA = 500
INITIAL_PLAYER_HP = 50
LOST_BATTLE = 0xFFFFFFFF


class Data:
    hp_boss: int
    damage: int

    def __init__( self, hp_boss: int, damage: int ):
        self.hp_boss = hp_boss
        self.damage = damage


type EffectApplyFn = Callable[ [ BattleStateBase ], None ]


class Spell:
    name: str  # For debug purposes
    cost: int
    time: int
    apply_fn: EffectApplyFn

    def __init__( self, name: str, cost: int, time: int, apply_fn: EffectApplyFn ):
        self.name = name
        self.cost = cost
        self.time = time
        self.apply_fn = apply_fn


class SpellEffect:
    spell: Spell
    timer: int

    def __init__( self, spell: Spell, timer: int ):
        self.spell = spell
        self.timer = timer


class BattleStateBase:
    hp_boss: int
    hp_player: int
    armor: int
    mana: int

    def __init__( self, hp_boss: int, hp_player: int, mana: int ):
        self.hp_boss = hp_boss
        self.hp_player = hp_player
        self.mana = mana
        self.armor = 0


class BattleState( BattleStateBase ):
    effects: list[ SpellEffect ]
    mana_spent: int
    turn_no: int  # For debug purposes

    def __init__(
            self,
            hp_boss: int,
            hp_player: int,
            mana: int,
            effects: list[ SpellEffect ],
            mana_spent: int,
            turn_no: int
    ):
        super().__init__( hp_boss, hp_player, mana )
        self.effects = [ SpellEffect( effect.spell, effect.timer ) for effect in effects ]
        self.mana_spent = mana_spent
        self.turn_no = turn_no

    def __str__( self ):
        active_spells = " ".join( f"{effect.spell.name}#{effect.timer} " for effect in self.effects )
        return (f"Player HP: {self.hp_player} / Boss HP: {self.hp_boss} / Player armor: {self.armor} / "
                f"Mana: {self.mana} / Mana spent: {self.mana_spent} / Active spells: {active_spells}")


def do_magic_missile( state: BattleStateBase ) -> None:
    state.hp_boss -= 4


def do_drain( state: BattleStateBase ) -> None:
    state.hp_boss -= 2
    state.hp_player += 2


def do_shield( state: BattleStateBase ) -> None:
    state.armor = 7


def do_poison( state: BattleStateBase ) -> None:
    state.hp_boss -= 3


def do_recharge( state: BattleStateBase ) -> None:
    state.mana += 101


SPELLS: list[ Spell ] = [
    Spell( "Magic Missile", 53, 1, do_magic_missile ),
    Spell( "Drain", 73, 1, do_drain ),
    Spell( "Shield", 113, 6, do_shield ),
    Spell( "Poison", 173, 6, do_poison ),
    Spell( "Recharge", 229, 5, do_recharge )
]


def parse_data( lines: list[ str ] ) -> Data:
    return Data(
            int( lines[ 0 ].split( ": " )[ 1 ] ),
            int( lines[ 1 ].split( ": " )[ 1 ] )
    )


def task1( data: Data ) -> int:
    return find_optimal_battle( data, False )


def task2( data: Data ) -> int:
    return find_optimal_battle( data, True )


def find_optimal_battle( data: Data, hard: bool ) -> int:
    initial_state: BattleState = BattleState( data.hp_boss, 50, 500, [ ], 0, 1 )
    min_mana = iterate_battle_turns( data, initial_state, 0, LOST_BATTLE, hard )
    return min_mana


def iterate_battle_turns(
        data: Data,
        state: BattleState,
        turn: int,
        min_found: int,
        hard: bool
) -> int:
    if turn == 0 and hard:
        state.hp_player -= 1
        if state.hp_player == 0:
            return LOST_BATTLE

    # Apply effects
    state.armor = 0
    for effect in state.effects:
        effect.spell.apply_fn( state )
        effect.timer -= 1

    if state.hp_boss <= 0:
        return state.mana_spent

    active_effects = purged_effects(state.effects)
    active_spells = [ effect.spell for effect in active_effects ]

    # Boss' turn
    if turn == 1:
        hit_value = single_hit( data.damage, state.armor )
        new_state = BattleState(
                state.hp_boss,
                state.hp_player - hit_value,
                state.mana,
                active_effects,
                state.mana_spent,
                state.turn_no + 1
        )
        if new_state.hp_player <= 0:
            return LOST_BATTLE
        return iterate_battle_turns( data, new_state, 0, min_found, hard )

    # Player's turn
    min_mana = min_found
    available_spells = [ s for s in SPELLS
                         if s.cost <= state.mana and state.mana_spent + s.cost < min_found and s not in active_spells ]
    for spell in available_spells:
        effects = active_effects.copy()
        effects.append( SpellEffect( spell, spell.time ) )
        new_state = BattleState(
                state.hp_boss,
                state.hp_player,
                state.mana - spell.cost,
                effects,
                state.mana_spent + spell.cost,
                state.turn_no + 1
        )
        mana_spent = iterate_battle_turns( data, new_state, 1, min_mana, hard )
        if mana_spent < min_mana:
            min_mana = mana_spent
    return min_mana


def single_hit( attacker_damage: int, defender_armor: int ) -> int:
    return max( attacker_damage - defender_armor, 1 )


def purged_effects( effects: list[ SpellEffect ] ) -> list[ SpellEffect ]:
    return list( effect for effect in effects if effect.timer > 0 )


def main():
    helper.verbose_level = 0
    exec_tasks(
            parse_data,
            task1,
            task2,
            read_file( '../data/input/year15/day15_22.in' ),
            900,
            1216
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
