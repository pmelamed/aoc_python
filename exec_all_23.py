import day23_20
import day23_22
import day23_23
import day23_24
import helper

if __name__ == '__main__':
    try:
        print( "-- 23' 20 ----------------------------------------------" )
        day23_20.main()
        print( "-- 23' 22 ----------------------------------------------" )
        day23_22.main()
        print( "-- 23' 23 ----------------------------------------------" )
        day23_23.main()
        print( "-- 23' 24 ----------------------------------------------" )
        day23_24.main()
    except Exception as ex:
        helper.print_ex( ex )
