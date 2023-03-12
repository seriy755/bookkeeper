"""
Модуль для описания представителя бюджета
"""
from typing import Any

from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.repository.abstract_repository import AbstractRepository

from bookkeeper.view.modal_windows import error_message


class BudgetPresenter():
    "Класс представителя бюджета"
    def __init__(self,
                 repo: AbstractRepository['Budget']) -> None:
        self.repo = repo
        self._data = repo.get_all()

        if not self._data:
            day = Budget(0, 'день', None, 1000.0)
            week = Budget(0, 'неделя', None, 7000.0)
            month = Budget(0, 'месяц', None, 30000.0)
            self.repo.add(day)
            self.repo.add(week)
            self.repo.add(month)
            self._data = repo.get_all()

    def data(self) -> list[list[Any]]:
        "Вернуть данные из репозитория в формате списка"
        data: list[list[Any]] = []
        for item in self._data:
            amount, restrict = item.amount, item.restrict
            data.append([amount, restrict])
        return data

    def update_data(self,
                    exp_repo: AbstractRepository['Expense']) -> None:
        "Обновить данные в репозитории"
        amounts = Budget.get_amounts(exp_repo)
        for budget, amount in zip(self._data, amounts):
            budget.amount = amount
            self.repo.update(budget)

    def update_restricts(self,
                         restricts: list[str]) -> None:
        "Обновить данные об ограничении на бюджет"
        for budget, restrict in zip(self._data, restricts):
            try:
                if float(restrict) < 0:
                    error_message("Ограничение на бюджет не может "
                                  "быть отрциательным!\n"
                                  "Пожалуйста, введите положительное число!")
                    continue
            except ValueError:
                error_message("Неверно указано ограничение на бюджет!\n"
                              "Пожалуйста, введите положительное число!")
                continue
            budget.restrict = float(restrict)
            self.repo.update(budget)
