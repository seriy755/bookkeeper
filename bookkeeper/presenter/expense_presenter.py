"""
Модуль для описания представителя расходов
"""
from typing import Any

from bookkeeper.models.expense import Expense
from bookkeeper.repository.abstract_repository import AbstractRepository


class ExpensePresenter():
    "Класс представителя расходов"
    def __init__(self,
                 repo: AbstractRepository['Expense']) -> None:
        self.repo = repo
        self._data = self.repo.get_all()

    def data(self) -> list[list[Any]]:
        "Вернуть данные из репозитория в формате списка"
        data: list[list[Any]] = []
        for item in self._data:
            amount, cat, date, comment = item.amount, item.category, \
                item.expense_date, item.comment
            data.append([date, amount, cat, comment])
        return data

    def add_data(self, amount: float, category: int) -> None:
        "Добавить данные в репозиторий"
        exp = Expense(amount=amount, category=category)
        self.repo.add(exp)
        self._data = self.repo.get_all()

    def get_all_pk(self) -> list[int]:
        "Получить список всех pk из таблциы"
        return list(exp.pk for exp in self._data)

    def delete_data(self, exp: Expense) -> None:
        "Удалить данные из репозитория"
        self.repo.delete(exp.pk)
        self._data = self.repo.get_all()

    def update_data(self, exp: Expense) -> None:
        "Обновить данные в репозитории"
        self.repo.update(exp)
        self._data = self.repo.get_all()

    def get(self, pk: int) -> Expense | None:
        "получить объект из репозитория по его pk"
        return self.repo.get(pk)

    def get_all(self,
                where: dict[str, Any] | None = None) -> list['Expense']:
        "Получить все записи из репозитория по некоторому условию"
        return self.repo.get_all(where)
