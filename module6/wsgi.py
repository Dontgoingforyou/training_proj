# http://localhost:5000/USD


import requests

from flask import Flask, jsonify

app = Flask(__name__)

def get_exchange_rate(currency: str):
    """ Функция для получения данных о курсе валюты """

    url = f"https://api.exchangerate-api.com/v4/latest/{currency.upper()}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None


@app.route('/<currency>', methods=['GET'])
def get_currency_rate(currency: str):
    """ Роут для получения курса валюты по отношению к доллару """

    data = get_exchange_rate(currency)
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Не удалось получить данные об обменном курсе"}), 500


if __name__ == '__main__':
    app.run(debug=True)