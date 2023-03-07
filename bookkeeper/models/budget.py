"""
Модель бюджета
"""

from dataclasses import dataclass
from datetime import datetime, timedelta

from bookkeeper.models.expense import Expense
from ..repository.abstract_repository import AbstractRepository


@dataclass
class Budget:
    """
    Бюджет.
    amount - сумма расходов
    category - id категории расходов
    limit - лимит расходов
    period- срок
    pk - id записи в базе данных
    """
    amount: int
    period: str
    category: int | None = None
    restrict: int | None = None
    pk: int = 0

    @classmethod
    def get_amounts(cls,
                    repo: AbstractRepository['Expense']) -> list[int]:
        "Функция для подсчёта суммы расходов за день, неделю, месяц"
        day_amount = 0
        date = datetime.now()
        day_expenses = repo.get_all(where={"expense_date":
                                           date.strftime('%Y-%m-%d')})
        day_amount += sum(exp.amount for exp in day_expenses)

        week_amount = 0
        for i in range(date.weekday() + 1):
            weekday = date - timedelta(days=i)
            weekday_expenses = repo.get_all(where={"expense_date":
                                                   weekday.strftime('%Y-%m-%d')})
            week_amount += sum(exp.amount for exp in weekday_expenses)

        month_amount = 0
        for i in range(date.day):
            monthday = date - timedelta(days=i)
            month_expenses = repo.get_all(where={"expense_date":
                                                 monthday.strftime('%Y-%m-%d')})
            month_amount += sum(exp.amount for exp in month_expenses)
        return [day_amount, week_amount, month_amount]

    @classmethod
    def create_from_restricts(
            cls,
            restricts: list[tuple[int | None, int | None]],
            repo: AbstractRepository['Expense']) -> list['Budget']:
        "Функция для создания списка бюджета из списка ограничений"
        periods = ('день', 'неделя', 'месяц')
        amounts = cls.get_amounts(repo)
        created: list[Budget] = []
        for values, period, amount in zip(restricts, periods, amounts):
            cat = values[0]
            restrict = values[1]
            budget = cls(amount, period, cat, restrict)
            created.append(budget)
        return created
