import re


CMD_PATTERN = re.compile( r"([a-z]{3}) (?:([ab])(?:, )?)?([+-][0-9]+)?" )
from typing import Callable

import helper
from helper import exec_tasks, print_ex, read_file


class State:
    a: int
    b: int
    ip: int

    def __init__( self ):
        self.a = 0
        self.b = 0
        self.ip = 0


type CommandFn = Callable[ [ State, int, int ], None ]


class Command:
    arg: int
    offset: int
    fn: CommandFn

    def __init__( self, arg: int, offset: int, fn: CommandFn ):
        self.arg = arg
        self.offset = offset
        self.fn = fn


def do_hlf( state: State, arg: int, _: int ) -> None:
    if arg == 0:
        state.a = state.a // 2
    else:
        state.b = state.b // 2
    state.ip += 1


def do_tpl( state: State, arg: int, _: int ) -> None:
    if arg == 0:
        state.a = state.a * 3
    else:
        state.b = state.b * 3
    state.ip += 1


def do_inc( state: State, arg: int, _: int ) -> None:
    if arg == 0:
        state.a += 1
    else:
        state.b += 1
    state.ip += 1


def do_jie( state: State, arg: int, offset: int ) -> None:
    value = state.a if arg == 0 else state.b
    if value % 2 == 0:
        state.ip += offset
    else:
        state.ip += 1


def do_jio( state: State, arg: int, offset: int ) -> None:
    value = state.a if arg == 0 else state.b
    if value == 1:
        state.ip += offset
    else:
        state.ip += 1


def do_jmp( state: State, _: int, offset: int ) -> None:
    state.ip += offset


def parse_data( lines: list[ str ] ) -> list[ Command ]:
    return [ parse_command( line ) for line in lines ]


def parse_command( line: str ) -> Command:
    m = CMD_PATTERN.match( line )
    name = m.group( 1 )
    arg = m.group( 2 )
    offset = m.group( 3 )
    match name:
        case "hlf":
            return Command( parse_arg( arg ), 0, do_hlf )
        case "tpl":
            return Command( parse_arg( arg ), 0, do_tpl )
        case "inc":
            return Command( parse_arg( arg ), 0, do_inc )
        case "jmp":
            return Command( 0, int( offset ), do_jmp )
        case "jie":
            return Command( parse_arg( arg ), int( offset ), do_jie )
        case "jio":
            return Command( parse_arg( arg ), int( offset ), do_jio )
    return Command( 0, 0, lambda _state, _arg, _offset: None )


def parse_arg( arg: str ) -> int:
    return 0 if arg == "a" else 1


def task1( program: list[ Command ] ) -> int:
    state = State()
    while state.ip < len( program ):
        cmd = program[ state.ip ]
        cmd.fn( state, cmd.arg, cmd.offset )
    return state.b


def task2( program: list[ Command ] ) -> int:
    state = State()
    state.a = 1
    while state.ip < len( program ):
        cmd = program[ state.ip ]
        cmd.fn( state, cmd.arg, cmd.offset )
    return state.b


def main():
    helper.verbose_level = 0
    exec_tasks(
            parse_data,
            task1,
            task2,
            read_file( '../data/input/year15/day15_23.in' ),
            170,
            247
    )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
