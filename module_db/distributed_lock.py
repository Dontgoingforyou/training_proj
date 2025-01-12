import datetime
import redis
import time
from multiprocessing import Process
from redis.exceptions import LockError
from functools import wraps

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def single(max_processing_time: datetime.timedelta):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Уникальный ключ для лока, основанный на имени функции
            lock_key = f"лок: {func.__module__}.{func.__name__}"
            lock = redis_client.lock(
                lock_key,
                timeout=int(max_processing_time.total_seconds()),  # Максимальная продолжительность лока
                blocking_timeout=5,  # Время ожидания лока
            )

            try:
                # захват лока
                if lock.acquire():
                    print(f"лок для {lock_key}")
                    result = func(*args, **kwargs)
                    return result
                else:
                    raise LockError(f"Не удалось получить лок для {lock_key}")
            finally:
                if lock.locked():
                    lock.release()
                    print(f"лок снят для {lock_key}")

        return wrapper
    return decorator


@single(max_processing_time=datetime.timedelta(minutes=2))
def critical_section():
    print("Запущена обработка...")
    time.sleep(2)
    print("Выполнено")

if __name__ == "__main__":
    # Проверка не параллельной работы функции
    processes = [Process(target=critical_section) for _ in range(3)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()