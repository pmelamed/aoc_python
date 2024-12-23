from typing import Optional

from helper import exec_task, exec_tasks, print_ex, read_file


class Computer:
    code: list[ int ]
    init_regs: list[ int ]
    regs: list[ int ]
    iptr: int = 0
    output: str = ""

    def __init__( self, code: list[ int ], regs: list[ int ] ):
        self.code = code
        self.init_regs = regs

    def combo_arg( self, arg: int ):
        if 0 <= arg <= 3: return arg
        if 4 <= arg <= 6: return self.regs[ arg - 4 ]
        raise NotImplemented( "Combo operand code 7 not supported" )

    def exec_op( self ):
        op = self.code[ self.iptr ]
        arg = self.code[ self.iptr + 1 ]
        self.iptr += 2
        match op:
            case 0:
                self.regs[ 0 ] = self.regs[ 0 ] // 2 ** self.combo_arg( arg )
            case 1:
                self.regs[ 1 ] = self.regs[ 1 ] ^ arg
            case 2:
                self.regs[ 1 ] = self.combo_arg( arg ) % 8
            case 3:
                if self.regs[ 0 ] != 0: self.iptr = arg
            case 4:
                self.regs[ 1 ] = self.regs[ 1 ] ^ self.regs[ 2 ]
            case 5:
                self.output += "," + str( self.combo_arg( arg ) % 8 )
            case 6:
                self.regs[ 1 ] = self.regs[ 0 ] // 2 ** self.combo_arg( arg )
            case 7:
                self.regs[ 2 ] = self.regs[ 0 ] // 2 ** self.combo_arg( arg )

    def is_halted( self ) -> bool:
        return self.iptr >= len( self.code )

    def reset( self, a: Optional[ int ] = None ):
        self.iptr = 0
        self.regs = self.init_regs.copy()
        self.output = ""
        if a is not None: self.regs[ 0 ] = a

    def exec( self, a: Optional[ int ] = None ) -> str:
        self.reset( a )
        while not self.is_halted(): self.exec_op()
        return self.output[ 1: ]

    def get_first_output( self, a: int ) -> str:
        self.reset( a )
        while len( self.output ) == 0 and not self.is_halted(): self.exec_op()
        return self.output[ 1: ]


def prepare( lines: list[ str ] ) -> Computer:
    return Computer( [ int( op ) for op in lines[ 4 ][ 9: ].split( "," ) ],
                     [ int( line[ 12: ] ) for line in lines[ :3 ] ] )


def task1( pc: Computer ) -> str:
    return pc.exec()


def task2( pc: Computer ) -> int:
    # 2,4 B = A % 8                 B=0, 0<A<8
    # 1,6 B = B ^ 6                 B=6
    # 7,5 C = A // 2 ** B           C=0
    # 4,6 B = B ^ C                 B=6
    # 1,4 B = B ^ 4                 B = 4
    # 5,5 OUT B % 8                 B = 0
    # 0,3 A = A // 8                A < 8
    # 3,0 JNC 0                     A = 0
    a = find_min_a( pc, 0, 0 )
    result = pc.exec( a )
    assert result == ",".join( map( str, pc.code ) )
    return a


def find_min_a( pc: Computer, digit: int, base_a: int ) -> Optional[ int ]:
    if digit == len( pc.code ): return base_a
    for modulus in range( 1 if digit == 0 else 0, 8 ):
        a = base_a * 8 + modulus
        # output = int( check_modulus_a( a ) )
        output = int( pc.get_first_output( a ) )
        expected = pc.code[ -digit - 1 ]
        if output == expected:
            result = find_min_a( pc, digit + 1, a )
            if result is not None: return result
    return None


def check_modulus_a( a: int ) -> int:
    b = a % 8
    b ^= 6
    c = a // 2 ** b
    b = b ^ c
    b ^= 4
    return b % 8


def main():
    exec_task( prepare, task1, read_file( 'data/day24_17.sample' ), "4,6,3,5,6,3,5,2,1,0" )
    exec_tasks( prepare, task1, task2,
                read_file( 'data/day24_17.in' ),
                "2,3,6,2,1,6,1,2,1",
                90938893795561 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
