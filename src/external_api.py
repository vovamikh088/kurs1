import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()
CUR_API_KEY = os.getenv("CUR_API_KEY")
STC_API_KEY = os.getenv("STC_API_KEY")

logger = logging.getLogger("external_api")
logger.setLevel(logging.INFO)
base_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(base_dir, "..", "logs")
log_file_path = os.path.join(log_dir, "external_api.log")
file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_currency(data):
    """Получает курсы валют относительно RUB через внешний API.

    Args:
        data (dict): Словарь с данными пользователя, включая список валют ("user_currencies").

    Returns:
        list: Список словарей с валютами и их курсами, например [{"currency": "USD", "rate": 90.5}].
    """
    print(data)
    currency_rates = []
    logger.info("Проходимся по списку валют пользователя")
    for i in data["user_currencies"]:
        try:
            url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={i}&amount=1"
            headers = {"apikey": CUR_API_KEY}
            response = requests.get(url, headers=headers)
            currency_rates.append({"currency": i, "rate": round(response.json()["result"], 2)})
            logger.info(
                'Добавляем словарь {"currency": "%s", "rate": %s} в список с ответами',
                i, round(response.json()["result"], 2)
            )
        except Exception as e:
            logger.error(f"Ошибка при API: {e}")
    return currency_rates


def get_stocks(data):
    """Получает текущие цены акций через внешний API.

    Args:
        data (dict): Словарь с данными пользователя, включая список акций ("user_stocks").

    Returns:
        list: Список словарей с тикерами акций и их ценами, например [{"stock": "AAPL", "price": 175.5}].
    """
    stock_prices = []
    logger.info("Проходимся по списку акций пользователя")
    for i in data["user_stocks"]:
        try:
            api_url = "https://api.api-ninjas.com/v1/stockprice?ticker={}".format(i)
            response = requests.get(api_url, headers={"X-Api-Key": STC_API_KEY})
            stock_prices.append({"stock": i, "price": response.json()["price"]})
            logger.info(f'Добавляем словарь {({"stock": i, "price": response.json()["price"]})} в список с ответами')
        except Exception as e:
            logger.error(f"Ошибка при API: {e}")
    return stock_prices
