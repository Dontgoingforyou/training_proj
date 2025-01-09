import random
import time
import json
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from multiprocessing import Pool, Process, Queue, cpu_count
import math
from typing import List


# Генерация данных
def generate_data(n: int) -> List[int]:
    return [random.randint(1, 1000) for _ in range(n)]


# Функция обработки числа
def process_number(number: int) -> bool:
    # Ресурсоёмкая операция: проверка числа на простоту
    if number < 2:
        return False
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True


# Однопоточная обработка
def single_thread_processing(data: List[int]) -> List[bool]:
    return [process_number(num) for num in data]


# Вариант A: ThreadPoolExecutor
def thread_pool_processing(data: List[int]) -> List[bool]:
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_number, data))
    return results


# Вариант B: multiprocessing.Pool
def multiprocessing_pool_processing(data: List[int]) -> List[bool]:
    with Pool(cpu_count()) as pool:
        results = pool.map(process_number, data)
    return results


# Вариант C: multiprocessing.Process + Queue
def process_worker(input_queue: Queue, output_queue: Queue) -> None:
    while not input_queue.empty():
        try:
            number = input_queue.get_nowait()
            result = process_number(number)
            output_queue.put(result)
        except Exception:
            break


def multiprocessing_process_queue(data: List[int]) -> List[bool]:
    input_queue = Queue()
    output_queue = Queue()

    for num in data:
        input_queue.put(num)

    processes = [Process(target=process_worker, args=(input_queue, output_queue)) for _ in range(cpu_count())]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    results = []
    while not output_queue.empty():
        results.append(output_queue.get())

    return results


# Измерение времени выполнения
def measure_time(func, data: List[int]) -> tuple[List[bool], float]:
    start_time = time.time()
    result = func(data)
    elapsed_time = time.time() - start_time
    return result, elapsed_time


# Сравнение производительности
def main() -> None:
    n = 5000  # Количество чисел для обработки
    data = generate_data(n)

    results = {}
    for name, func in [
        ("Single Thread", single_thread_processing),
        ("ThreadPoolExecutor", thread_pool_processing),
        ("Multiprocessing.Pool", multiprocessing_pool_processing),
        ("Multiprocessing.Process + Queue", multiprocessing_process_queue),
    ]:
        print(f"Запуск {name}...")
        _, elapsed_time = measure_time(func, data)
        results[name] = elapsed_time

    # Сохранение результатов в JSON
    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)

    print("Результаты сравнения:")
    for method, time_taken in results.items():
        print(f"{method}: {time_taken:.2f} секунд")


if __name__ == "__main__":
    main()
