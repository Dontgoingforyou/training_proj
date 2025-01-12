import random
import time
import redis

class RateLimitExceed(Exception):
    """ Исключение, выбрасываемое при превышении лимита запросов """
    pass


class RateLimiter:
    def __init__(self, redis_client, key='rate_limiter', limit=5, window=3):
        """
        Инициализация ограничителя скорости.
        :param redis_client - экземпляр Redis клиента.
        :param key - ключ в Redis для хранения данных.
        :param limit - максимальное количество запросов за окно времени.
        :param window - окно времени (в секундах).
        """

        self.redis = redis_client
        self.key = key
        self.limit = limit
        self.window = window

    def test(self) -> bool:
        """
        Проверяет, достигнут ли лимит запросов.
        :return: True, если лимит не превышен иначе False.
        """

        current_time = int(time.time())

        with self.redis.pipeline() as pipe:
            pipe.zadd(self.key, {current_time: current_time})  # Добавление текущего запроса с временной меткой
            pipe.zremrangebyscore(self.key, 0, current_time - self.window)  # Удаление запросов старше `window` секунд
            pipe.zcard(self.key)  # Получение количества запросов за последние `window` секунд
            pipe.expire(self.key, self.window)  # Установка TTL ключа
            _, _, count, _ = pipe.execute()

        return random.randint(1, 5) != 1


def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        # какая-то бизнес логика
        print("Запрос выполнен")


if __name__ == '__main__':
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    rate_limiter = RateLimiter(redis_client)

    for _ in range(50): # Имитация 50 запросов
        time.sleep(random.randint(1, 2)) # Случайная задержка между запросами

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")

