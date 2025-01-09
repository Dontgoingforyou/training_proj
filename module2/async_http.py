import aiohttp
import asyncio
import json
from aiohttp import ClientSession
from asyncio import Semaphore


async def fetch_url(url: str, session: ClientSession, semaphore: Semaphore) -> dict:
    """Асинхронная функция для выполнения HTTP-запроса с обработкой ошибок."""

    async with semaphore:
        try:
            async with session.get(url, timeout=10) as response:
                return {"url": url, "status_code": response.status}
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return {"url": url, "status_code": 0}


async def fetch_urls(urls: list[str], file_path: str):
    """Асинхронная функция для выполнения запросов по списку URL-ов."""

    semaphore = Semaphore(5)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(url, session, semaphore) for url in urls]
        results = await asyncio.gather(*tasks)

        with open(file_path, 'w', encoding='utf-8') as file:
            for result in results:
                file.write(json.dumps(result) + '\n')


if __name__ == '__main__':
    urls = [
        "https://example.com",
        "https://httpbin.org/status/404",
        "https://nonexistent.url"
    ]
    asyncio.run(fetch_urls(urls, './results.jsonl'))
