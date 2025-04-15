import logging
import os
from typing import Any, Hashable, Union

import pandas as pd

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
base_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(base_dir, "..", "logs")
log_file_path = os.path.join(log_dir, "utils.log")
file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def XLSX_file_read() -> Union[list[dict[Hashable, Any]], str]:
    """Читает данные из XLSX-файла и преобразует их в список словарей.

    Returns:
        Список словарей с данными транзакций или строку с ошибкой, если файл не найден.
        :return:
    """
    logger.info("Задаём путь до файла")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "data")
    file_path = os.path.join(data_dir, "operations.xlsx")
    try:
        logger.info("Переводим XLSX файл в json формат")
        df = pd.read_excel(file_path)
        fixed_df = df.dropna(subset=["Номер карты"])
        list_of_dicts = fixed_df.to_dict(orient="records")
        return list_of_dicts
    except FileNotFoundError:
        logger.error("Ошибка, файл не найден")
        return "Файл не найден"


def file_df():
    """Читает данные из XLSX-файла и возвращает их в виде DataFrame.

    Returns:
        DataFrame с данными транзакций или строку с ошибкой, если файл не найден.
    """
    logger.info("Задаём путь до файла")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "data")
    file_path = os.path.join(data_dir, "operations.xlsx")
    try:
        logger.info("Переводим XLSX файл в DataFrame формат")
        df = pd.read_excel(file_path)
        fixed_df = df.dropna(subset=["Номер карты"])
        return fixed_df
    except FileNotFoundError:
        logger.error("Ошибка, файл не найден")
        return "Файл не найден"
