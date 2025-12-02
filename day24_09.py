from typing import TypeAlias

import helper


FileInfo: TypeAlias = tuple[ int, int, int ]  # ID, Position, Length
SpaceInfo: TypeAlias = tuple[ int, int ]  # Position, Length


class Data:
    files: list[ FileInfo ]
    spaces: list[ SpaceInfo ]

    def __init__(
            self,
            files: list[ FileInfo ],
            empty: list[ SpaceInfo ]
            ):
        self.files = files
        self.spaces = empty


def prepare( lines: list[ str ] ) -> Data:
    files: list[ FileInfo ] = list()
    empty: list[ SpaceInfo ] = list()
    disk_map = bytearray( lines[ 0 ], "UTF-8" )
    file_id = 0
    position = 0
    is_file = True
    for cell in [ c - ord( '0' ) for c in disk_map ]:
        if is_file:
            files.append( (file_id, position, cell) )
            file_id += 1
        else:
            empty.append( (position, cell) )
        position += cell
        is_file = not is_file
    return Data( files, empty )


def task1( data: Data ) -> int:
    spaces = data.spaces.copy()
    files = data.files.copy()
    spaces.reverse()
    result = 0
    while len( spaces ) > 0 and len( files ) > 0 and files[ -1 ][ 1 ] > spaces[ -1 ][ 0 ]:
        file, space, increase = move_file( files.pop(), spaces.pop() )
        result += increase
        if file[ 2 ] != 0:
            files.append( file )
        if space[ 1 ] != 0:
            spaces.append( space )
    for file in files:
        result += sum( [ file[ 0 ] * pos for pos in range( file[ 1 ], file[ 1 ] + file[ 2 ] ) ] )
    return result


def task2( data: Data ) -> int:
    spaces = data.spaces.copy()
    files = data.files.copy()
    files.reverse()
    moved_files: list[ FileInfo ] = list()
    result = 0
    for file in files:
        index: int = find_target_space( file, spaces )
        if index == -1:
            moved_files.append( file )
        else:
            space = spaces[ index ]
            moved_files.append( (file[ 0 ], space[ 0 ], file[ 2 ]) )
            if space[ 1 ] > file[ 2 ]:
                spaces[ index ] = (space[ 0 ] + file[ 2 ], space[ 1 ] - file[ 2 ])
            else:
                del spaces[ index ]

    for file in moved_files:
        result += sum( [ file[ 0 ] * pos for pos in range( file[ 1 ], file[ 1 ] + file[ 2 ] ) ] )
    return result


def move_file( file: FileInfo, empty: SpaceInfo ) -> tuple[ FileInfo, SpaceInfo, int ]:
    moved_cells = min( file[ 2 ], empty[ 1 ] )
    return (
        (file[ 0 ], file[ 1 ], file[ 2 ] - moved_cells),
        (empty[ 0 ] + moved_cells, empty[ 1 ] - moved_cells),
        sum( file[ 0 ] * pos for pos in range( empty[ 0 ], empty[ 0 ] + moved_cells ) )
    )


def find_target_space( file: FileInfo, spaces: list[ SpaceInfo ] ) -> int:
    index = 0
    while index < len( spaces ) and spaces[ index ][ 0 ] < file[ 1 ]:
        if spaces[ index ][ 1 ] >= file[ 2 ]:
            return index
        index += 1
    return -1


def main():
    helper.exec_tasks( prepare, task1, task2, [ "2333133121414131402" ], 1928, 2858 )
    helper.exec_tasks( prepare, task1, task2, helper.read_file( 'data/day24_09.in' ), 6378826667552, 6413328569890 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        helper.print_ex( ex )
