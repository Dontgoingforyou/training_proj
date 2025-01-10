import aiohttp
import asyncio
import json
import aiofiles
from aiohttp import ClientSession
from asyncio import Semaphore, Queue


async def fetch_url(url: str, session: ClientSession, semaphore: Semaphore) -> dict:
    """Асинхронная функция для выполнения HTTP-запроса с обработкой ошибок."""

    async with semaphore:
        print(f"Старт запроса: {url}")
        try:
            async with session.get(url, timeout=10) as response:
                print(f"Завершен запрос: {url} со статусом {response.status}")
                return {"url": url, "status_code": response.status}
        except (aiohttp.ClientError, asyncio.TimeoutError):
            print(f"Ошибка при запросе: {url}")
            return {"url": url, "status_code": 0}


async def worker(queue: Queue, session: ClientSession, semaphore: Semaphore, file_path: str):
    """Функция воркера, которая обрабатывает URL из очереди."""

    while True:
        url = await queue.get()
        if url is None:  # Завершающий сигнал
            break
        result = await fetch_url(url, session, semaphore)

        async with aiofiles.open(file_path, 'a', encoding='utf-8') as file:
            await file.write(json.dumps(result) + '\n')
        queue.task_done()


async def fetch_urls(urls: list[str], file_path: str):
    """Асинхронная функция для выполнения запросов по списку URL-ов с ограничением."""

    semaphore = Semaphore(5)
    queue = Queue()
    num_workers = 5  # Количество воркеров

    with open(file_path, 'w', encoding='utf-8') as file:
        pass

    async with aiohttp.ClientSession() as session:
        # Заполняем очередь URL-ами
        for url in urls:
            await queue.put(url)

        # Запуск воркеров
        workers = [
            asyncio.create_task(worker(queue, session, semaphore, file_path))
            for _ in range(num_workers)
        ]

        # Ожидание обработки всех URL-ов
        await queue.join()

        # Отправление завершения воркерам
        for _ in range(num_workers):
            await queue.put(None)

        # Ожидание завершения всех воркеров
        await asyncio.gather(*workers)


if __name__ == '__main__':

    urls = [f"https://httpbin.org/status/{code}" for code in range(200, 230)]
    urls.extend([
        "https://example.com",
        "https://httpbin.org/status/404",
        "https://nonexistent.url"
    ])
    urls *= 10
    asyncio.run(fetch_urls(urls, './results.jsonl'))