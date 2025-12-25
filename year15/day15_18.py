from geom2d import Field2D, STAR_DIRS_2D, Coord2D
from helper import exec_tasks, print_ex, read_file, SYM_OBSTACLE

CORNERS = {
    Coord2D.from_coords(0, 0),
    Coord2D.from_coords(0, 99),
    Coord2D.from_coords(99, 0),
    Coord2D.from_coords(99, 99)
}


def parse_data(lines: list[str]) -> Field2D[bool]:
    return Field2D.from_input(lines, cell_t=lambda cell_ch: cell_ch == SYM_OBSTACLE)


def task1(data: Field2D[bool], steps: int) -> int:
    field: Field2D[bool] = data
    for i in range(steps):
        next_gen = Field2D.from_value(field.width, field.height, False)
        for x, y in field.range():
            coord = Coord2D.from_coords(x, y)
            own_state = field[coord]
            neighbours_on = field.count_around(coord, lambda cell: cell, STAR_DIRS_2D)
            next_gen[coord] = ((own_state and (neighbours_on == 2 or neighbours_on == 3))
                               or (not own_state and neighbours_on == 3))
        field = next_gen
    return field.count_if(lambda _x, _y, cell: cell)


def task2(data: Field2D[bool], steps: int) -> int:
    field: Field2D[bool] = data.copy()
    for pt in CORNERS:
        field[pt] = True
    for i in range(steps):
        next_gen = Field2D.from_value(field.width, field.height, False)
        for pt in CORNERS:
            next_gen[pt] = True
        for x, y in field.range():
            coord = Coord2D.from_coords(x, y)
            if coord in CORNERS:
                continue
            own_state = field[coord]
            neighbours_on = field.count_around(coord, lambda cell: cell, STAR_DIRS_2D)
            next_gen[coord] = (own_state and (neighbours_on == 2 or neighbours_on == 3)
                               or (not own_state and neighbours_on == 3))
        field = next_gen
    return field.count_if(lambda _x, _y, cell: cell)


def main():
    exec_tasks(parse_data,
               lambda d: task1(d, 100),
               lambda d: task2(d, 100),
               read_file('../data/input/year15/day15_18.in'),
               814,
               924)


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print_ex(ex)
