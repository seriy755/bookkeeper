"""
Тесты GUI для модуля с моделью таблицы
"""
from PySide6.QtCore import Qt

from bookkeeper.view.table_model import TableModel


def test_create_table_model(qtbot):
    data = [
            ["2023-03-13", 123.0, 'Сыр', ''],
            ["2023-03-13", 266.0, 'Колбаса', '']
        ]
    columns = 'Дата Сумма Категория Комментарий'.split()
    edit_indexes = list(range(4))

    table = TableModel(data, columns, None, edit_indexes)
    assert table.columnCount() == 4
    assert table.rowCount() == 2


def test_data(qtbot):
    data = [
            ["2023-03-13", 123.0, 'Сыр', ''],
            ["2023-03-13", 266.0, 'Колбаса', '']
        ]
    columns = 'Дата Сумма Категория Комментарий'.split()
    edit_indexes = list(range(4))

    table = TableModel(data, columns, None, edit_indexes)
    index = table.index(1, 1)
    assert index.isValid()

    value = table.data(index)
    assert float(value) == 266.0


def test_flags(qtbot):
    data = [
            ["2023-03-13", 123.0, 'Сыр', ''],
            ["2023-03-13", 266.0, 'Колбаса', '']
        ]
    columns = 'Дата Сумма Категория Комментарий'.split()
    edit_indexes = []

    table = TableModel(data, columns, None, edit_indexes)
    index = table.index(1, 1)
    assert table.flags(index) == Qt.ItemIsEnabled | Qt.ItemIsSelectable


def test_set_data(qtbot):
    data = [
            ["2023-03-13", 123.0, 'Сыр', ''],
            ["2023-03-13", 266.0, 'Колбаса', '']
        ]
    columns = 'Дата Сумма Категория Комментарий'.split()
    edit_indexes = [1, 2, 3]

    table = TableModel(data, columns, None, edit_indexes)
    index = table.index(1, 1)
    value = 300
    assert table.setData(index, value)
    assert not table.setData(index, value, Qt.DisplayRole)
