"""
Тесты GUI для модуля с главным окном приложения
"""
from pytestqt.qt_compat import qt_api

from bookkeeper.view.main_window import MainWindow


def test_function():
    pass


def test_create_main_window(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)


def test_set_expense_grid(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)

    data = [
            ["2023-03-13", 123.0, 'Сыр', ''],
            ["2023-03-13", 266.0, 'Колбаса', '']
        ]
    ids = [1, 2]
    widget.set_expense_grid(data, ids)
    assert len(widget.get_all_expenses()) == 2


def test_set_budget_grid(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)

    data = [[10, 15],
            [20, 90],
            [50, 300]]
    widget.set_budget_grid(data)
    assert len(widget.get_all_restricts()) == 3


def test_set_category_dropdown(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)

    data = [[1, 'Продукты'], [2, 'Фрукты']]
    widget.set_category_dropdown(data)
    assert widget.category_dropdown.count() == 2


def test_get_data(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)

    assert len(widget.get_selected_expense()) == 0
    assert widget.get_amount() == '0'
    assert widget.get_selected_cat() is None


def test_show_category_editor_window(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)

    assert widget.show_category_editor_window([]) is None


def test_buttons_clicked(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)

    widget.on_expense_add_button_clicked(test_function)
    qtbot.mouseClick(
        widget.expense_add_button,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )

    widget.on_expense_delete_button_clicked(test_function)
    qtbot.mouseClick(
        widget.expense_delete_button,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )

    widget.on_expense_save_changes_button_clicked(test_function)
    qtbot.mouseClick(
        widget.expense_save_changes_button,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )

    widget.on_category_edit_button_clicked(test_function)
    qtbot.mouseClick(
        widget.category_edit_button,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )
