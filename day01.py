import re

import helper


class Data:
    list1 = [ ]
    list2 = [ ]

    def __init__( self, list1, list2 ):
        self.list1 = list1
        self.list2 = list2


def prepare( lines ):
    list1 = [ ]
    list2 = [ ]
    for line in lines:
        nums = [ int( num_str ) for num_str in re.findall( "[0-9]+", line ) ]
        list1.append( nums[ 0 ] )
        list2.append( nums[ 1 ] )
    list1.sort()
    list2.sort()
    return Data( list1, list2 )


def task1( data ):
    list1 = data.list1
    list2 = data.list2
    sum_distance = 0
    for distance in [ abs( list1[ index ] - list2[ index ] ) for index in range( len( list1 ) ) ]:
        sum_distance += distance
    return sum_distance


def task2( data ):
    list1 = data.list1.copy()
    list1.append( -1 )
    list2 = data.list2.copy()
    list2.append( -1 )
    index1 = 0
    index2 = 0
    sum_distance = 0
    list1_len = len( list1 ) - 1
    list2_len = len( list2 ) - 1
    while index1 < list1_len and index2 < list2_len:
        base = list1[ index1 ]
        if base == list2[ index2 ]:
            count1 = 0
            while list1[ index1 ] == base:
                count1 += 1
                index1 += 1
            count2 = 0
            while list2[ index2 ] == base:
                count2 += 1
                index2 += 1
            sum_distance += count1 * base * count2
        else:
            if base < list2[ index2 ]:
                index1 += 1
            else:
                index2 += 1
    return sum_distance


if __name__ == '__main__':
    try:
        helper.exec_tasks_file( prepare, task1, task2, 'data/day01.sample', 11, 31 )
        helper.exec_tasks_file( prepare, task1, task2, 'data/day01.in', 765748, 27732508 )
    except Exception as ex:
        helper.print_ex( ex )
