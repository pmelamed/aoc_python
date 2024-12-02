import sys
import traceback
from collections.abc import Callable, Iterable


def task_check( func: Callable[ [ object ], str | int ], data: object, sample: str | int ):
    result = func(data)
    if sample is None:
        print(f"\x1b[1;5;30;100m RESULT \x1b[0m - {result}")
    else:
        if result == sample:
            print(f"\x1b[1;5;30;42m   OK   \x1b[0m - {result} == {sample}")
        else:
            print(f"\x1b[1;5;30;41m  FAIL  \x1b[0m - {result} != {sample}")


def exec_tasks_file( prepare_fn: Callable[ [ Iterable[ str ] ], object ],
                     task1_fn: Callable[ [object], str | int ],
                     task2_fn: Callable[ [object], str | int ],
                     file_name: str,
                     check_value1: str | int,
                     check_value2: str | int ):
    data = open(file_name)
    try:
        exec_tasks(prepare_fn, task1_fn, task2_fn, data, check_value1, check_value2)
    finally:
        data.close()


def exec_tasks( prepare_fn: Callable[ [ Iterable[ str ] ], object ],
                task1_fn: Callable[ [object], str | int ],
                task2_fn: Callable[ [ object], str | int ],
                data: Iterable[ str ],
                check_value1: str | int,
                check_value2: str | int ):
    if prepare_fn is not None:
        data = prepare_fn(data)
    task_check(task1_fn, data, check_value1)
    task_check(task2_fn, data, check_value2)


def print_ex( ex: Exception ):
    [ print( line, file=sys.stderr ) for line in traceback.format_exception( ex ) ]
