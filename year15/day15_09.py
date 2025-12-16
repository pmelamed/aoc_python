from collections import defaultdict

from helper import exec_tasks, print_ex, read_file


# City# -> [(City#, Distance)]
type Data = dict[ int, list[ tuple[ int, int ] ] ]


def parse_data( lines: list[ str ] ) -> Data:
    city_numbers: dict[ str, int ] = dict()
    data: Data = defaultdict( lambda: list() )
    for line in lines:
        city1, _, city2, _, distance_str = tuple( line.split( " " ) )
        if city1 not in city_numbers:
            city_numbers[ city1 ] = len( city_numbers )
        if city2 not in city_numbers:
            city_numbers[ city2 ] = len( city_numbers )
        city1_number = city_numbers[ city1 ]
        city2_number = city_numbers[ city2 ]
        data[ city1_number ].append( (city2_number, int( distance_str )) )
        data[ city2_number ].append( (city1_number, int( distance_str )) )
    for city_data in data.values():
        city_data.sort( key = lambda city: city[ 1 ] )
    return data


def task1( data: Data ) -> int:
    min_found = -1
    for city in range( len( data ) ):
        new_found = find_min_way( data, city, { city }, 0, min_found )
        if min_found < 0 or new_found < min_found:
            min_found = new_found
    return min_found


def task2( data: Data ) -> int:
    max_found = -1
    for city in range( len( data ) ):
        new_found = find_max_way( data, city, { city }, 0 )
        if new_found > max_found:
            max_found = new_found
    return max_found


def find_min_way(
        data: Data,
        last_visited: int,
        cities_visited: set[ int ],
        passed_distance: int,
        min_found: int
) -> int:
    if len( cities_visited ) == len( data ):
        return passed_distance
    min_distance = min_found
    for city, distance in data[ last_visited ]:
        if city in cities_visited:
            continue
        new_distance = distance + passed_distance
        if 0 < min_distance <= new_distance:
            continue
        cities_visited.add( city )
        new_found_path = find_min_way( data, city, cities_visited, new_distance, min_distance )
        cities_visited.remove( city )
        if min_distance < 0 or new_found_path < min_distance:
            min_distance = new_found_path
    return min_distance


def find_max_way(
        data: Data,
        last_visited: int,
        cities_visited: set[ int ],
        passed_distance: int
) -> int:
    if len( cities_visited ) == len( data ):
        return passed_distance
    max_distance = 0
    for city, distance in data[ last_visited ]:
        if city in cities_visited:
            continue
        new_distance = distance + passed_distance
        cities_visited.add( city )
        new_found_path = find_max_way( data, city, cities_visited, new_distance )
        cities_visited.remove( city )
        if new_found_path > max_distance:
            max_distance = new_found_path
    return max_distance


def main():
    exec_tasks( parse_data, task1, task2, read_file( '../data/samples/year15/day15_09.sample' ), 605, 982 )
    exec_tasks( parse_data, task1, task2, read_file( '../data/input/year15/day15_09.in' ), 141, 736 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
