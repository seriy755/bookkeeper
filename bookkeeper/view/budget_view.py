"""
Модуль для описания графического интерфейса
таблицы бюджета
"""
# pylint: disable = no-name-in-module
# mypy: disable-error-code="attr-defined,union-attr"
from typing import Union, Any

from PySide6.QtWidgets import QTableView, QHeaderView

from bookkeeper.view.table_model import TableModel
from bookkeeper.view.modal_windows import message_send


class BudgetTableView(QTableView):
    "Графическое представление бюджета"
    def __init__(self) -> None:
        super().__init__()
        self.item_model: Union[None, TableModel] = None

    def set_budget_table(self,
                         data: list[list[Any]],
                         update: bool = False) -> None:
        "Установить модель таблицы бюджета"
        columns = 'Сумма Бюджет'.split()
        rows = 'День Неделя Месяц'.split()
        edit_indexes = [1]
        self.item_model = TableModel(data, columns, rows, edit_indexes)
        self.setModel(self.item_model)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if update is True:
            self._is_checked_amount(data)

    def _is_checked_amount(self,
                           data: list[list[Any]]) -> None:
        "Проверка на превышение лимита затрат за день/неделю/месяц"
        for row, value in enumerate(data):
            period = ('день' if row == 0 else 'неделю' if row == 1
                      else 'месяц')
            if value[0] > value[1]:
                message_send(f"Превышен лимит бюджета на {period}!")

    def get_all_restricts(self) -> list[str]:
        "Получить все ограничения из таблицы"
        data: list[str] = []
        if self.item_model is None:
            return data
        for row in range(self.item_model.rowCount()):
            data.append(self.item_model.index(row, 1).data())
        return data
