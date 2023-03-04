"""
Модуль для описания таблицы расходов
"""

from PySide6.QtWidgets import QTableView, QHeaderView
from PySide6 import QtCore
from PySide6.QtCore import Qt

from datetime import datetime


class TableModel(QtCore.QAbstractTableModel):
    "Модель таблицы"
    def __init__(self, data, columns):
        super(TableModel, self).__init__()
        self._data = data
        self._columns = columns

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, datetime):
                return value.strftime('%Y-%m-%d')
            if isinstance(value, float):
                return f'{value:.2f}'
            return value
        
    def headerData(self, section: int, orientation: Qt.Orientation, 
                   role: int = Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._columns[section].title()

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])


class ExpenseTableView(QTableView):
    "Графическое представление бюджета"
    def __init__(self):
        super(ExpenseTableView, self).__init__()
        
    def set_expense_table(self, data):
        columns = 'Дата Сумма Категория Комментарий'.split()
        self.item_model = TableModel(data, columns)
        self.setModel(self.item_model)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().hide()
        