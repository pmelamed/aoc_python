import day15_01
import day15_02
import day15_03
import day15_04
import day15_05
import helper


if __name__ == '__main__':
    try:
        print( "-- 15' 01 ----------------------------------------------" )
        day15_01.main()
        print( "-- 15' 02 ----------------------------------------------" )
        day15_02.main()
        print( "-- 15' 03 ----------------------------------------------" )
        day15_03.main()
        print( "-- 15' 04 ----------------------------------------------" )
        day15_04.main()
        print( "-- 15' 05 ----------------------------------------------" )
        day15_05.main()
    except Exception as ex:
        helper.print_ex( ex )
