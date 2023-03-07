"""
Модуль для описания таблицы бюджета
"""

from typing import Union, Any

from PySide6.QtWidgets import QTableView, QHeaderView

from bookkeeper.view.table_model import TableModel


class BudgetTableView(QTableView):
    "Графическое представление бюджета"
    def __init__(self) -> None:
        super().__init__()

    def set_budget_table(self,
                         data: list[list[Any]]) -> None:
        "Установить модель таблицы бюджета"
        columns = 'Сумма Бюджет'.split()
        rows = 'День Неделя Месяц'.split()
        edit_indexes = [1]
        self.item_model = TableModel(data, columns, rows, edit_indexes)
        self.setModel(self.item_model)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def get_selected_expense(self) -> int:
        "Получить номер выбанной записи"
        self.itemDoubleClicked.connect(onClickItem)
    
    def get_all_restricts(self) -> list[str]:
        data: list[str] = []
        for row in range(self.item_model.rowCount()):
            data.append(self.item_model.index(row, 1).data())
        return data
    