import concurrent.futures

from .services import fetch_task, process_task


def worker(worker_id: int):
    """ Воркер извлекает и обрабатывает задачи """

    while True:
        task = fetch_task(worker_id)
        if not task:
            print(f'Воркер {worker_id}: Нет задач')
            break
        process_task(task)


def main():
    """ Запуска нескольких воркеров параллельно """
    num_workers = 4
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        executor.map(worker, range(1, num_workers + 1))