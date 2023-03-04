"""
Модуль для описания таблицы бюджета
"""

from PySide6.QtWidgets import QTableView, QHeaderView
from PySide6 import QtCore
from PySide6.QtCore import Qt

                
class TableModel(QtCore.QAbstractTableModel):
    "Модель таблицы"
    def __init__(self, data, columns, rows):
        super(TableModel, self).__init__()
        self._data = data
        self._columns = columns
        self._rows = rows

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, float):
                return f'{value:.2f}'
            return value
        
    def headerData(self, section: int, orientation: Qt.Orientation, 
                   role: int = Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._columns[section].title()
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._rows[section].title()

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])
                
                
class BudgetTableView(QTableView):
    "Графическое представление бюджета"
    def __init__(self):
        super(BudgetTableView, self).__init__()
        
    def set_budget_table(self, data):
        columns = 'Сумма Бюджет'.split()
        rows = 'День Неделя Месяц'.split()
        self.item_model = TableModel(data, columns, rows)
        self.setModel(self.item_model)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
