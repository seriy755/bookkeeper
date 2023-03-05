"""
Модель бюджета
"""

from dataclasses import dataclass
from datetime import datetime, timedelta

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
    category: int | None
    restrict: int
    period: str
    pk: int = 0
    
    
    def get_amounts(repo: AbstractRepository['Expense']) -> list[int]:
        """
        Посчитать сумму расходов за день, неделю, месяц
        """ 
        day_amount = 0
        date = datetime.now()
        day_expenses = repo.get_all(where={"expense_date":
                                           date.strftime('%Y-%m-%d')})
        day_amount += sum([exp.amount for exp in day_expenses])
        
        week_amount = 0
        for i in range(date.weekday() + 1):
            weekday = date - timedelta(days=i)
            weekday_expenses = repo.get_all(where={"expense_date":
                                                   weekday.strftime('%Y-%m-%d')})
            week_amount += sum([exp.amount for exp in weekday_expenses])
        
        month_amount = 0 
        for i in range(date.day):
            monthday = date - timedelta(days=i)
            month_expenses = repo.get_all(where={"expense_date":
                                                 monthday.strftime('%Y-%m-%d')})
            month_amount += sum([exp.amount for exp in month_expenses])
        return [day_amount, week_amount, month_amount]
           
    
    @classmethod
    def create_from_list(
            cls,
            restricts: list[tuple[int | None, int]],
            repo: AbstractRepository['Expense']):
        periods = ('день', 'неделя', 'месяц')
        amounts = cls.get_amounts(repo)
        created: list[Budget] = []
        for values, period, amount in zip(restricts, periods, amounts):
            cat = values[0]
            restrict = values[1]
            budg = cls(amount, cat, restrict, period)
            created.append(budg)
        return created
            