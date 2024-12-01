def task_check(func, data, sample):
    result = func(data)
    if sample is None:
        print(f"RESULT {result}")
    else:
        if result == sample:
            print(f"OK   - {result} == {sample}")
        else:
            print(f"FAIL - {result} != {sample}")


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
