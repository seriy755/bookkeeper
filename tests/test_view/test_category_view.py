"""
Тесты GUI для модуля с категориями расходов
"""
from pytestqt.qt_compat import qt_api

from bookkeeper.view.category_view import CategoryEditorWindow


def test_function():
    pass


def test_create_category_editor(qtbot):
    widget = CategoryEditorWindow()
    qtbot.addWidget(widget)
    assert widget.model is None


def test_init_model(qtbot):
    widget = CategoryEditorWindow()
    qtbot.addWidget(widget)

    widget._init_model()
    assert widget.model is not None

    widget._init_model()
    assert widget.model is not None


def test_update_data(qtbot):
    widget = CategoryEditorWindow()
    qtbot.addWidget(widget)

    data = [[1, 'Продукты', None],
            [2, 'Фрукты', 1]]
    widget.update_data(data)

    for i in range(len(data)):
        assert widget._data[i] == data[i]


def test_get_data(qtbot):
    widget = CategoryEditorWindow()
    qtbot.addWidget(widget)

    names = widget.get_all_names()
    assert names == []

    data = [[1, 'Продукты', None],
            [2, 'Фрукты', 1]]
    widget.update_data(data)
    widget_data = widget.get_all_categories()
    assert data == widget_data

    widget.new_category_line_edit.setText('Апельсин')
    new_category = widget.get_new_category()
    assert new_category == 'Апельсин'

    names = widget.get_all_names()
    assert names == ['Продукты', 'Фрукты']

    parent = widget.get_selected_category()
    assert parent is None

    index = widget.model.index(0, 0)
    assert index.isValid()

    widget.tree.setCurrentIndex(index)
    parent = widget.get_selected_category()
    assert parent is not None


def test_buttons_clicked(qtbot):
    widget = CategoryEditorWindow()
    qtbot.addWidget(widget)

    widget.on_category_add_button_clicked(test_function)
    qtbot.mouseClick(
        widget.category_add_button,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )

    widget.on_category_delete_button_clicked(test_function)
    qtbot.mouseClick(
        widget.category_delete_button,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )

    widget.on_category_save_changes_button_clicked(test_function)
    qtbot.mouseClick(
        widget.category_save_changes_button,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )
