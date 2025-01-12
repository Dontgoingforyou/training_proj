import redis
import json


class RedisQueue:
    def __init__(self, name='default_queue', host='localhost', port=6379, db=0):
        """ Инициализация Redis подключения и имени очереди """

        self._redis = redis.StrictRedis(host=host, port=port, db=db)
        self._name = name

    def publish(self, msg: dict):
        """ Добавляет сообщение в очередь """

        serialized_msg = json.dumps(msg)  # Сериализация сообщения в строку
        self._redis.lpush(self._name, serialized_msg)

    def consume(self) -> dict:
        """ Извлекает сообщение из очереди """

        serialized_msg = self._redis.rpop(self._name)  # Удаление элемента с конца очереди
        if serialized_msg is None:
            return None  # Очередь пуста
        return json.loads(serialized_msg)  # Десериализация сообщения


if __name__ == '__main__':
    q = RedisQueue(name='test_queue')

    q.publish({'a': 1})
    q.publish({'b': 2})
    q.publish({'c': 3})

    assert q.consume() == {'a': 1}
    assert q.consume() == {'b': 2}
    assert q.consume() == {'c': 3}
    print("Все работает!")