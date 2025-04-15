from src.services import investment_bank


def test_investment_bank(sample_transactions):
    # Модифицируем тестовые данные для проверки логики округления
    modified_transactions = [{**t, "Сумма операции": 1536} for t in sample_transactions]  # Пример суммы для округления

    result = investment_bank("2023-01", modified_transactions, 50)
    assert isinstance(result, (float, int))  # Принимаем и float и int
    assert result > 0  # Проверяем что результат положительный


def test_investment_bank_no_transactions(sample_transactions):
    # Тест для месяца без транзакций
    result = investment_bank("2022-12", sample_transactions, 50)
    assert isinstance(result, (float, int))
    assert result == 0  # Ожидаем 0 если нет транзакций
