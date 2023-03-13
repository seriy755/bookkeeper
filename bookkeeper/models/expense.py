"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    added_date - дата добавления в бд
    comment - комментарий
    pk - id записи в базе данных
    """
    amount: float
    category: int
    expense_date: str = datetime.now().strftime('%Y-%m-%d')
    added_date: str = datetime.now().strftime('%Y-%m-%d')
    comment: str = ''
    pk: int = 0
