import json

from helper import exec_tasks, first_line, print_ex, read_file

ALLOWED_CHARS = "abcdefghjkmnpqrstuvwxyz"
ALLOWED_CHARS_COUNT = len( ALLOWED_CHARS )


def task1( data: str ) -> int:
    # result = 0
    # index = 0
    # number = ""
    # while index < len( data ):
    #     ch = data[ index ]
    #     while ord( '0' ) <= ord( ch ) <= ord( '9' ) or ch == "-":
    #         number += ch
    #         index += 1
    #         ch = data[ index ]
    #     if number != "":
    #         result += int( number )
    #         number = ""
    #     index += 1
    # return result
    return count_numbers( json.loads( data ), False )


def task2( data: str ) -> int:
    return count_numbers( json.loads( data ), True )


def count_numbers( obj, red_rule ) -> int:
    sub_objects = [ ]
    result = 0
    if type( obj ).__name__ == "dict":
        for item in obj.items():
            if red_rule and item[ 1 ] == "red":
                return 0
            if type( item[ 1 ] ).__name__ == "int":
                result += item[ 1 ]
            else:
                sub_objects.append( item[ 1 ] )
    elif type( obj ).__name__ == "list":
        for item in obj:
            if type( item ).__name__ == "int":
                result += item
            else:
                sub_objects.append( item )
    return result + sum( count_numbers( sub_obj, red_rule ) for sub_obj in sub_objects )


def main():
    exec_tasks( first_line, task1, task2, read_file( '../data/input/year15/day15_12.in' ), 111754, 65402 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
