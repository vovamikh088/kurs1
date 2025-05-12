# type: ignore
import json

import pytest

from src.views import get_cards, get_top_transactions, main_sheet

# Тестовые данные
TEST_XLSX_DATA = [
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


@pytest.fixture
def mock_xlsx_file_read(monkeypatch):
    def mock_return(*args, **kwargs):
        return TEST_XLSX_DATA

    monkeypatch.setattr("src.views.XLSX_file_read", mock_return)


def test_get_top_transactions():
    # Тестируем получение топ-5 транзакций
    result = get_top_transactions(TEST_XLSX_DATA)

    # Проверяем, что возвращается 5 транзакций
    assert len(result) == 5

    # Проверяем, что транзакции отсортированы по убыванию суммы
    amounts = [tx["amount"] for tx in result]
    assert amounts == sorted(amounts, reverse=True)

    # Проверяем структуру данных
    for tx in result:
        assert "date" in tx
        assert "amount" in tx
        assert "category" in tx
        assert "description" in tx


def test_get_cards():
    # Тестируем агрегацию данных по картам
    result = get_cards(TEST_XLSX_DATA)

    # Проверяем, что найдены все карты
    assert len(result) == 2

    # Проверяем правильность подсчета сумм и кешбэка
    for card in result:
        if card["last_digits"] == "234567890123456":
            assert card["total_spent"] == 3000.0  # 1000 + 500 + 1500
            assert card["cashback"] == 135.0  # 50 + 10 + 75
        elif card["last_digits"] == "876543210987654":
            assert card["total_spent"] == 4800.0  # 2000 + 300 + 2500
            assert card["cashback"] == 240.0  # 100 + 15 + 125

    # Проверяем структуру данных
    for card in result:
        assert "last_digits" in card
        assert "total_spent" in card
        assert "cashback" in card


def test_main_sheet_structure(mock_xlsx_file_read, mock_currency_api, mock_stocks_api, mock_user_settings_file):
    # Тестируем общую структуру ответа
    result = json.loads(main_sheet("2023-01-10 12:00:00"))

    # Проверяем наличие всех ожидаемых ключей
    assert "greeting" in result
    assert "cards" in result
    assert "top_transactions" in result
    assert "currency_rates" in result
    assert "stock_prices" in result

    # Проверяем типы данных
    assert isinstance(result["greeting"], str)
    assert isinstance(result["cards"], list)
    assert isinstance(result["top_transactions"], list)
    assert isinstance(result["currency_rates"], list)
    assert isinstance(result["stock_prices"], list)

    # Проверяем, что данные карт соответствуют ожиданиям
    assert len(result["cards"]) == 2
    for card in result["cards"]:
        assert "last_digits" in card
        assert "total_spent" in card
        assert "cashback" in card

    # Проверяем, что топ транзакций отсортированы правильно
    amounts = [tx["amount"] for tx in result["top_transactions"]]
    assert amounts == sorted(amounts, reverse=True)
