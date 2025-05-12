# type: ignore
import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category(sample_df):
    # Изменяем суммы операций на отрицательные (расходы)
    sample_df["Сумма операции"] = [-100, -200, -300]
    sample_df["Сумма операции с округлением"] = [-100, -200, -300]

    result = spending_by_category(sample_df, "Еда", "2023-01-10")
    assert isinstance(result, pd.DataFrame)
    assert "Еда" in result.columns
    # Проверяем что сумма отрицательная и преобразуем np.int64 к int
    assert int(result["Еда"].iloc[0]) < 0


def test_spending_by_category_default_date(sample_df):
    # Аналогично делаем суммы отрицательными
    sample_df["Сумма операции"] = [-100, -200, -300]
    sample_df["Сумма операции с округлением"] = [-100, -200, -300]

    result = spending_by_category(sample_df, "Еда")
    assert isinstance(result, pd.DataFrame)
    assert "Еда" in result.columns
