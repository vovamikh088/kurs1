import logging
import os
from datetime import datetime
from src.views import main_sheet
from src.reports import spending_by_category
from src.services import investment_bank, description_filter
from src.utils import XLSX_file_read, file_df


def setup_logging():
    """Настройка базового логирования для main"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler('main.log', mode='w', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


def main():
    setup_logging()
    logger = logging.getLogger("main")
    logger.info("Запуск приложения")

    try:
        # 1. Пример использования main_sheet
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        financial_report = main_sheet(current_date)
        print("\nФинансовый отчет:")
        print(financial_report)

        # 2. Пример работы с отчетами
        transactions_df = file_df()
        if isinstance(transactions_df, pd.DataFrame):
            spending_report = spending_by_category(transactions_df, "Супермаркеты")
            print("\nОтчет по расходам в категории 'Супермаркеты':")
            print(spending_report)

        # 3. Пример работы с сервисами
        transactions_list = XLSX_file_read()
        if isinstance(transactions_list, list):
            # Анализ инвестиций
            potential_income = investment_bank("2023-10", transactions_list, 50)
            print(f"\nПотенциальный доход от округления: {potential_income} руб.")

            # Фильтрация транзакций
            filtered = description_filter(transactions_list, "ашан")
            print("\nТранзакции, связанные с 'ашан':")
            print(filtered)

    except Exception as e:
        logger.error(f"Ошибка в работе приложения: {e}")

    logger.info("Завершение работы приложения")


if __name__ == "__main__":
    main()