import day25_01
import day25_02
import day25_03
import helper


if __name__ == '__main__':
    try:
        print( "-- 25' 01 ----------------------------------------------" )
        day25_01.main()
        print( "-- 25' 02 ----------------------------------------------" )
        day25_02.main()
        print( "-- 25' 03 ----------------------------------------------" )
        day25_03.main()
    except Exception as ex:
        helper.print_ex( ex )
