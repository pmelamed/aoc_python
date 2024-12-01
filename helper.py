def task_check(func, data, sample):
    result = func(data)
    if sample is None:
        print(f"\x1b[1;5;30;100m RESULT \x1b[0m - {result}")
    else:
        if result == sample:
            print(f"\x1b[1;5;30;42m   OK   \x1b[0m - {result} == {sample}")
        else:
            print(f"\x1b[1;5;30;41m  FAIL  \x1b[0m - {result} != {sample}")


def exec_tasks_file(prepare_fn, task1_fn, task2_fn, file_name, check_value1, check_value2):
    data = open(file_name)
    try:
        exec_tasks(prepare_fn, task1_fn, task2_fn, data, check_value1, check_value2)
    finally:
        data.close()


def exec_tasks(prepare_fn, task1_fn, task2_fn, data, check_value1, check_value2):
    if prepare_fn is not None:
        data = prepare_fn(data)
    task_check(task1_fn, data, check_value1)
    task_check(task2_fn, data, check_value2)
