from time import time


def time_tracker(fn):
    """Декоратор для подсчета времени выполнения функции"""
    def wrapper(*args, **kwargs) -> str:
        start_time = time()
        fn(*args, **kwargs)
        res_time = time() - start_time
        print(f'Функция отработала за {res_time} сек.')
    return wrapper
