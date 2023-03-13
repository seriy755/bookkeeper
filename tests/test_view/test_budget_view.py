"""
Тесты GUI для модуля с таблицей бюджета
"""
from PySide6.QtWidgets import QMessageBox

from bookkeeper.view.budget_view import BudgetTableView


def test_create_budget_grid(qtbot):
    widget = BudgetTableView()
    qtbot.addWidget(widget)
    assert widget.item_model is None


def test_set_budget_table(qtbot):
    widget = BudgetTableView()
    qtbot.addWidget(widget)

    data = [[10, 15],
            [20, 90],
            [50, 300]]
    widget.set_budget_table(data)
    assert widget.item_model is not None


def test_msg_box(qtbot, monkeypatch):
    widget = BudgetTableView()
    qtbot.addWidget(widget)

    data = [[20, 15],
            [20, 90],
            [50, 300]]
    monkeypatch.setattr(QMessageBox, 'exec',
                        lambda *args: QMessageBox.Ok)
    assert widget.set_budget_table(data, True) is None


def test_get_all_restricts(qtbot):
    widget = BudgetTableView()
    qtbot.addWidget(widget)

    assert widget.get_all_restricts() == []

    data = [[10, 15],
            [20, 90],
            [50, 300]]
    widget.set_budget_table(data)
    assert len(widget.get_all_restricts()) == 3
