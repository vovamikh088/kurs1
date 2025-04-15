import json

import pytest
import pandas as pd
from unittest.mock import patch, mock_open


@pytest.fixture
def sample_transactions():
    return [
        {
            "Номер карты": "1234567890121234",
            "Сумма операции": 100.0,
            "Сумма операции с округлением": 100.0,
            "Категория": "Еда",
            "Описание": "Обед",
            "Дата операции": "01.01.2023 12:00:00",
            "Дата платежа": "01.01.2023",
            "Кэшбэк": 1.0,
        },
        {
            "Номер карты": "1234567890121234",
            "Сумма операции": 200.0,
            "Сумма операции с округлением": 200.0,
            "Категория": "Транспорт",
            "Описание": "Такси",
            "Дата операции": "02.01.2023 12:00:00",
            "Дата платежа": "02.01.2023",
            "Кэшбэк": 2.0,
        },
        {
            "Номер карты": "1234567890125678",
            "Сумма операции": 300.0,
            "Сумма операции с округлением": 300.0,
            "Категория": "Еда",
            "Описание": "Ужин",
            "Дата операции": "03.01.2023 12:00:00",
            "Дата платежа": "03.01.2023",
            "Кэшбэк": 3.0,
        },
    ]


@pytest.fixture
def mock_currency_api(monkeypatch):
    def mock_return(*args, **kwargs):
        return [{"currency": "USD", "rate": 75.0}, {"currency": "EUR", "rate": 85.0}]

    monkeypatch.setattr("src.views.get_currency", mock_return)


@pytest.fixture
def mock_stocks_api(monkeypatch):
    def mock_return(*args, **kwargs):
        return [{"stock": "AAPL", "price": 150.0}, {"stock": "GOOGL", "price": 2500.0}]

    monkeypatch.setattr("src.views.get_stocks", mock_return)


@pytest.fixture
def mock_user_settings_file():
    with patch("builtins.open", mock_open(
                   read_data=json.dumps({"currencies": ["USD", "EUR"],
                                         "stocks": ["AAPL", "GOOGL"]}))):
        yield


@pytest.fixture
def sample_df(sample_transactions):
    return pd.DataFrame(sample_transactions)


@pytest.fixture
def user_settings():
    return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]}


@pytest.fixture
def mock_requests(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        if "exchangerates_data" in args[0]:
            return MockResponse({"result": 75.5}, 200)
        elif "api-ninjas" in args[0]:
            return MockResponse({"price": 150.75}, 200)
        return MockResponse(None, 404)

    monkeypatch.setattr("requests.get", mock_get)


@pytest.fixture
def mock_xlsx_file_read(monkeypatch):
    def mock_return(*args, **kwargs):
        return [
            {
                "Дата платежа": "01.01.2023",
                "Дата операции": "2023-01-01 12:00:00",
                "Номер карты": "1234567890123456",
                "Сумма операции с округлением": 1000.0,
                "Категория": "Еда",
                "Описание": "Ресторан",
                "Кэшбэк": 50.0,
            },
            {
                "Дата платежа": "02.01.2023",
                "Дата операции": "2023-01-02 14:00:00",
                "Номер карты": "1234567890123456",
                "Сумма операции с округлением": 500.0,
                "Категория": "Транспорт",
                "Описание": "Такси",
                "Кэшбэк": 10.0,
            },
            {
                "Дата платежа": "03.01.2023",
                "Дата операции": "2023-01-03 16:00:00",
                "Номер карты": "9876543210987654",
                "Сумма операции с округлением": 2000.0,
                "Категория": "Одежда",
                "Описание": "Магазин",
                "Кэшбэк": 100.0,
            },
            {
                "Дата платежа": "04.01.2023",
                "Дата операции": "2023-01-04 18:00:00",
                "Номер карты": "9876543210987654",
                "Сумма операции с округлением": 300.0,
                "Категория": "Развлечения",
                "Описание": "Кино",
                "Кэшбэк": 15.0,
            },
            {
                "Дата платежа": "05.01.2023",
                "Дата операции": "2023-01-05 20:00:00",
                "Номер карты": "1234567890123456",
                "Сумма операции с округлением": 1500.0,
                "Категория": "Путешествия",
                "Описание": "Отель",
                "Кэшбэк": 75.0,
            },
            {
                "Дата платежа": "06.01.2023",
                "Дата операции": "2023-01-06 22:00:00",
                "Номер карты": "9876543210987654",
                "Сумма операции с округлением": 2500.0,
                "Категория": "Техника",
                "Описание": "Ноутбук",
                "Кэшбэк": 125.0,
            },
        ]

    monkeypatch.setattr("views.XLSX_file_read", mock_return)
