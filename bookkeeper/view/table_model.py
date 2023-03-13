"""
Модуль для описания модели таблицы.
Используется для отображения списка
расходов и бюджета
"""
from typing import Union, Any

from PySide6.QtCore import (QAbstractTableModel, QModelIndex,
                            QPersistentModelIndex, Qt)


class TableModel(QAbstractTableModel):
    "Модель таблицы"
    def __init__(self, data: list[list[Any]],
                 columns: list[str], rows: list[str] | None,
                 edit_indexes: list[int]):
        super().__init__()
        self._data = data
        self._columns = columns
        self.edit_indexes = edit_indexes
        if rows is None:
            row_count = self.rowCount()
            self._rows = list(str(i) for i in range(row_count))
        else:
            self._rows = rows

    def data(self, index: Union[QModelIndex, QPersistentModelIndex],
             role: int = Qt.EditRole | Qt.DisplayRole) -> Any:
        if role in (Qt.DisplayRole, Qt.EditRole):
            value = self._data[index.row()][index.column()]
            if isinstance(value, float):
                return f'{value:.2f}'
            return value

    def headerData(self, section: int,
                   orientation: Qt.Orientation,
                   role: int = Qt.DisplayRole) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._columns[section]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._rows[section]

    def rowCount(self,
                 parent: Union[QModelIndex, QPersistentModelIndex] = ...
                 ) -> int:
        return len(self._data) if self._data else 0

    def columnCount(self,
                    parent: Union[QModelIndex, QPersistentModelIndex] = ...
                    ) -> int:
        return len(self._data[0]) if self._data else 0

    def flags(self, index: Union[QModelIndex, QPersistentModelIndex]) -> Any:
        if index.column() in self.edit_indexes:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self, index: Union[QModelIndex, QPersistentModelIndex],
                value: Any,
                role: int = Qt.EditRole) -> bool:
        if role == Qt.EditRole:
            row = index.row()
            col = index.column()
            self._data[row][col] = value
            return True
        return False
