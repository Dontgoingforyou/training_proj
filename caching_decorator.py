import unittest.mock
from functools import wraps
from collections import OrderedDict

def lru_cache(*args, **kwargs):

    # Определение, был ли передан maxsize
    maxsize = kwargs.get('maxsize', None)

    def decorator(func):
        cache = OrderedDict()  # Сохранение порядка вставки

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Генерация ключа из аргументов
            key = (args, frozenset(kwargs.items()))

            # Если ключ уже есть, перемещение его в конец как недавно использованный
            if key in cache:
                cache.move_to_end(key)
                return cache[key]

            # Вызов основной функции и сохранение результата в кэш
            result = func(*args, **kwargs)
            cache[key] = result

            # Если размер кэша превышает maxsize, происходит удаление старого элемента
            if maxsize is not None and len(cache) > maxsize:
                cache.popitem(last=False)
            return result

        return wrapper

    # Если декоратор вызван без аргументов
    if len(args) == 1 and callable(args[0]) and not kwargs:
        return decorator(args[0])

    return decorator

@lru_cache
def sum(a: int, b: int) -> int:
    return a + b


@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == '__main__':
    assert sum(1, 2) == 3
    assert sum(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12

    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]

    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4