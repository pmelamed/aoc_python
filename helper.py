import sys
import traceback
from collections.abc import Callable, Iterable


def task_check[DataT, ResultT: str | int]( func: Callable[ [ DataT ], ResultT ], data: DataT, sample: ResultT ):
    result = func(data)
    if sample is None:
        print(f"\x1b[1;5;30;100m RESULT \x1b[0m - {result}")
    else:
        if result == sample:
            print(f"\x1b[1;5;30;42m   OK   \x1b[0m - {result} == {sample}")
        else:
            print(f"\x1b[1;5;30;41m  FAIL  \x1b[0m - {result} != {sample}")


def exec_tasks_file[ DataT, ResultT1: str | int, ResultT2: str | int ](
        prepare_fn: Callable[ [ Iterable[ str ] ], DataT ],
        task1_fn: Callable[ [ DataT ], ResultT1 ],
        task2_fn: Callable[ [ DataT ], ResultT2 ],
        file_name: str,
        check_value1: ResultT1,
        check_value2: ResultT2 ):
    data = open(file_name)
    try:
        exec_tasks(prepare_fn, task1_fn, task2_fn, data, check_value1, check_value2)
    finally:
        data.close()


def exec_tasks[ DataT, ResultT1: str | int, ResultT2: str | int ](
        prepare_fn: Callable[ [ Iterable[ str ] ], DataT ],
        task1_fn: Callable[ [ DataT ], ResultT1 ],
        task2_fn: Callable[ [ DataT ], ResultT2 ],
        data: Iterable[str],
        check_value1: ResultT1,
        check_value2: ResultT2 ):
    if prepare_fn is not None:
        data = prepare_fn(data)
    task_check(task1_fn, data, check_value1)
    task_check(task2_fn, data, check_value2)


def print_ex( ex: Exception ):
    [ print( line, file=sys.stderr ) for line in traceback.format_exception( ex ) ]
