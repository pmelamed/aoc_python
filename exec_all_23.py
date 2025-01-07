import day23_20
import day23_22
import helper

if __name__ == '__main__':
    try:
        print( "-- 23' 20 ----------------------------------------------" )
        day23_20.main()
        print( "-- 23' 22 ----------------------------------------------" )
        day23_22.main()
    except Exception as ex:
        helper.print_ex( ex )
