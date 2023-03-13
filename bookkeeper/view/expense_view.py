"""
Модуль для описания графического интерфейса
таблицы расходов
"""
from typing import Union, Any

from PySide6.QtWidgets import QTableView, QHeaderView

from bookkeeper.view.table_model import TableModel


class ExpenseTableView(QTableView):
    "Графическое представление расходов"
    def __init__(self) -> None:
        super().__init__()
        self.item_model: Union[None, TableModel] = None
        self.ids: list[int] = []

    def set_expense_table(self,
                          data: list[list[Any]],
                          ids: list[int]) -> None:
        "Установить модель таблицы расходов"
        columns = 'Дата Сумма Категория Комментарий'.split()
        edit_indexes = list(range(4))
        self.item_model = TableModel(data[::-1], columns,
                                     None, edit_indexes)
        self.setModel(self.item_model)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().hide()
        self.ids = ids[::-1]

    def get_selected_expense(self) -> set[int]:
        "Получить номер выбанной записи"
        indexes = self.selectedIndexes()
        return set(self.ids[int(index.row())] for index in indexes)

    def get_all_expenses(self) -> list[list[Any]]:
        "Получить все записи о расходах"
        data: list[list[Any]] = []
        if self.item_model is None:
            return data
        for row in range(self.item_model.rowCount()):
            row_data: list[Any] = [self.ids[row]]
            for column in range(self.item_model.columnCount()):
                row_data.append(self.item_model.index(row, column).data())
            data.append(row_data)
        return data
