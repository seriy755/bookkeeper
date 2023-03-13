"""
Тесты GUI для модуля с записями расходов
"""
from bookkeeper.view.expense_view import ExpenseTableView


def test_create_expense_grid(qtbot):
    widget = ExpenseTableView()
    qtbot.addWidget(widget)
    assert widget.item_model is None


def test_set_expense_table(qtbot):
    widget = ExpenseTableView()
    qtbot.addWidget(widget)

    data = [
            ["2023-03-13", 123.0, 'Сыр', ''],
            ["2023-03-13", 266.0, 'Колбаса', '']
        ]
    ids = [1, 2]
    widget.set_expense_table(data, ids)
    assert widget.item_model is not None


def test_get_all_expenses(qtbot):
    widget = ExpenseTableView()
    qtbot.addWidget(widget)

    assert widget.get_all_expenses() == []

    data = [
            ["2023-03-13", 123, 'Сыр', ''],
            ["2023-03-13", 266, 'Колбаса', '']
        ]
    ids = [1, 2]
    widget.set_expense_table(data, ids)
    widget.get_all_expenses() == data


def test_get_selected_expense(qtbot):
    widget = ExpenseTableView()
    qtbot.addWidget(widget)

    assert len(widget.get_selected_expense()) == 0

    data = [
            ["2023-03-13", 123, 'Сыр', ''],
            ["2023-03-13", 266, 'Колбаса', '']
        ]
    ids = [1, 2]
    widget.set_expense_table(data, ids)
    index = widget.item_model.index(0, 0)
    assert index.isValid()

    widget.setCurrentIndex(index)
    assert widget.get_selected_expense() == {2}
