import day24_01
import day24_02
import day24_03
import day24_04
import day24_05
import helper

if __name__ == '__main__':
    try:
        print( "-- 24' 01 ----------------------------------------------" )
        day24_01.main()
        print( "-- 24' 02 ----------------------------------------------" )
        day24_02.main()
        print( "-- 24' 03 ----------------------------------------------" )
        day24_03.main()
        print( "-- 24' 04 ----------------------------------------------" )
        day24_04.main()
        print( "-- 24' 05 ----------------------------------------------" )
        day24_05.main()
    except Exception as ex:
        helper.print_ex( ex )
