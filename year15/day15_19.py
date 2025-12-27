from helper import exec_tasks, print_ex, read_file


NOT_FOUND = 0xFFFFFFFF


class Data:
    source: str
    transforms: list[ tuple[ str, str ] ]

    def __init__( self, data: list[ str ] ) -> None:
        self.source = data[ -1 ]
        self.transforms = [ tuple( line.split( " => " ) ) for line in data[ :-2 ] ]


def task1( data: Data ) -> int:
    transformed: set[ str ] = set()
    for source, transform in data.transforms:
        index = data.source.find( source )
        while index >= 0:
            transformed.add( data.source[ :index ] + transform + data.source[ index + len( source ): ] )
            index = data.source.find( source, index + 1 )
    return len( transformed )


def task2( data: Data ) -> int:
    # transforms = sorted( data.transforms, key = lambda tpl: len( tpl[ 1 ] ), reverse = True )
    # formula = data.source
    # steps = iterate_candidates( transforms, formula, 0, NOT_FOUND, set() )
    # return iterate_generations( transforms, formula )
    return frontal_reduce( data )


def frontal_reduce( data: Data ) -> int:
    formula = data.source
    step = 0
    while formula != "e":
        start_step = step
        for tr_src, tr_tgt in data.transforms:
            modified = formula.replace( tr_tgt, tr_src, 1 )
            if modified != formula:
                formula = modified
                step += 1
                # break
        if start_step == step:
            print( f"Stuck at {formula}" )
            return NOT_FOUND
    return step


def iterate_generations( transforms: list[ tuple[ str, str ] ], formula: str ) -> int:
    steps = 0
    curr_gen: set[ str ] = { formula }
    while True:
        print( f"Generation: {steps:<4}  Candidates: {len( curr_gen )}" )
        next_gen: set[ str ] = set()
        for s in curr_gen:
            if s == "e":
                return steps
            for tr_index, tr_from, tr_to in get_all_candidates( transforms, s ):
                ns = s[ :tr_index ] + tr_to + s[ tr_index + len( tr_from ): ]
                next_gen.add( ns )
        curr_gen = next_gen
        steps += 1


def iterate_candidates(
        transforms: list[ tuple[ str, str ] ],
        s: str,
        steps: int,
        min_steps_found: int,
        cache: set[ str ]
) -> int:
    # print( f"Checking steps: {steps}, min_steps_found: {min_steps_found}")
    if steps >= min_steps_found:
        return NOT_FOUND
    if s == "e":
        print( f"Way found: {steps}" )
        return steps
    if s in cache:
        return NOT_FOUND
    cache.add( s )
    min_steps = min_steps_found
    for tr_index, tr_from, tr_to in get_all_candidates( transforms, s ):
        new_str = s[ :tr_index ] + tr_to + s[ tr_index + len( tr_from ): ]
        min_steps = min( min_steps, iterate_candidates( transforms, new_str, steps + 1, min_steps, cache ) )
    return min_steps


def get_all_candidates( transforms: list[ tuple[ str, str ] ], s: str ) -> list[ tuple[ int, str, str ] ]:
    result = [ ]
    for src, tgt in transforms:
        index = 0
        while index >= 0:
            index = s.find( tgt, index )
            if index >= 0:
                result.append( (index, tgt, src) )
                index += 1
    # print( f"Found {len(result)} candidates for '{s}'")
    return result


def main():
    exec_tasks( Data, task1, task2, read_file( '../data/input/year15/day15_19.in' ), 509, 195 )


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex( ex )
