# uvicorn module6.asgi:app --reload
# http://localhost:8000/USD


import httpx

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()


class ExchangeRateResponse(BaseModel):
    provider: str
    WARNING_UPGRADE_TO_V6: str
    terms: str
    base: str
    date: str
    time_last_updated: int
    rates: Dict[str, float]


async def get_exchange_rate(currency: str) -> ExchangeRateResponse:
    """ Асинхронная функция для получения данных о курсе валюты """

    url = f'https://api.exchangerate-api.com/v4/latest/{currency.upper()}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        if response.status_code == 200:
            data = response.json()
            return ExchangeRateResponse(**data)
        else:
            raise HTTPException(status_code=500, detail='Не удалось получить данные об обменном курсе')


@app.get('/{currency}', response_model=ExchangeRateResponse)
async def get_currency_rate(currency: str):
    """ Роут для получения курса валюты по отношению к доллару """
    return await get_exchange_rate(currency)
