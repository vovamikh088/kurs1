# type: ignore
from src.external_api import get_currency, get_stocks


def test_get_currency_success(mock_requests, user_settings):
    result = get_currency(user_settings)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["currency"] == "USD"
    assert result[0]["rate"] == 75.5


def test_get_stocks_success(mock_requests, user_settings):
    result = get_stocks(user_settings)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["stock"] == "AAPL"
    assert result[0]["price"] == 150.75
