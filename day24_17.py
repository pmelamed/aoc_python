from helper import print_ex, exec_tasks, read_file


class Computer:
    code: list[ int ]
    regs: list[ int ]
    iptr: int = 0
    output: str = ""

    def __init__( self, code: list[ int ], regs: list[ int ] ):
        self.code = code
        self.regs = regs.copy()

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


def prepare( lines: list[ str ] ) -> Computer:
    return Computer( [ int( op ) for op in lines[ 4 ][ 9: ].split( "," ) ],
                     [ int( line[ 12: ] ) for line in lines[ :3 ] ] )


def task1( pc: Computer ) -> str:
    while not pc.is_halted(): pc.exec_op()
    return pc.output[ 1: ]


def task2( pc: Computer ) -> str:
    return ""


def main():
    exec_tasks( prepare, task1, task2, read_file( 'data/day24_17.sample' ), "4,6,3,5,6,3,5,2,1,0", None )
    exec_tasks( prepare, task1, task2, read_file( 'data/day24_17.in' ), None, None )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
