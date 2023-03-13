"""
Модуль для описания графического интерфейса
окна редактирования списка категорий. Вывод
на экран таблицы расходов и элементов ввода
и редактирования таблиц:
поле ввода новой категории
кнопка редактирования категорий
кнопка добаления расхода
кнопка удаления расхода
кнопка сохранения изменений
"""
# pylint: disable = no-name-in-module
# pylint: disable = too-many-instance-attributes
# mypy: disable-error-code="attr-defined,union-attr,assignment,arg-type,call-arg"
from typing import Union, Callable, Any

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import (QVBoxLayout, QWidget, QGridLayout,
                               QTreeView, QPushButton, QLineEdit,
                               QAbstractItemView)


class CategoryEditorWindow(QWidget):
    "Класс для окна редактирования списка категорий"
    def __init__(self) -> None:
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tree = QTreeView(
            self,
            selectionMode=QAbstractItemView.SingleSelection)
        self.layout.addWidget(self.tree)

        bottom_controls = QGridLayout()
        self.model: Union[None, QStandardItemModel] = None

        self._data: list[list[Any]] = []

        self.new_category_line_edit = QLineEdit()
        self.new_category_line_edit.setPlaceholderText('Новая категория')
        bottom_controls.addWidget(self.new_category_line_edit, 0, 0)

        self.category_add_button = QPushButton('Добавить')
        bottom_controls.addWidget(self.category_add_button, 1, 0)
        self.category_delete_button = QPushButton('Удалить выбранную категорию')
        bottom_controls.addWidget(self.category_delete_button, 2, 0)
        self.category_save_changes_button = QPushButton('Сохранить изменения')
        bottom_controls.addWidget(self.category_save_changes_button, 3, 0)

        bottom_widget = QWidget()
        bottom_widget.setLayout(bottom_controls)
        self.layout.addWidget(bottom_widget)

    def _init_model(self) -> None:
        "Инициализировать модель"
        if self.model:
            self.model.clear()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Категория'])
        self.tree.setModel(self.model)
        self.tree.expandAll()

    def _sort_data(self, data: list[list[Any]],
                   parent: int | None = None) -> list[list[Any]]:
        "Отсортиовать данные в порядке топологической сортировки"
        new_data: list[list[Any]] = []
        for value in data:
            pk, name, pid = value
            if pid == parent:
                new_data.append([pk, name, pid])
                new_data += self._sort_data(data, pk)
        return new_data

    def update_data(self,
                    data: list[list[Any]]) -> None:
        "Обновить данные о списке категорий в модели"
        seen: dict[int, QStandardItem] = {}
        self._init_model()
        self._data = self._sort_data(data)
        for value in self._data:
            pk, name, parent = value

            if parent is None:
                parent = self.model.invisibleRootItem()
            else:
                parent = seen[parent]

            parent.appendRow([
                QStandardItem(name)])
            seen[pk] = parent.child(parent.rowCount() - 1)

    def get_new_category(self) -> str:
        "Получить имя новой категории"
        return str(self.new_category_line_edit.text())

    def get_selected_category(self) -> str | None:
        "Получить имя выбранной в модели категории"
        try:
            return str(self.tree.selectedIndexes()[0].data())
        except IndexError:
            return None

    def get_all_names(self,
                      parent: QModelIndex = QModelIndex()) -> list[str]:
        "Получить все имена из модели категорий"
        names: list[str] = []
        if self.model is None:
            return names
        row_count = self.model.rowCount(parent)
        for row in range(row_count):
            index: QModelIndex = self.model.index(row, 0, parent)
            names.append(self.model.data(index))
            if self.model.hasChildren(index):
                names += self.get_all_names(index)
        return names

    def get_all_categories(self) -> list[list[Any]]:
        "Получить все категории"
        names = self.get_all_names()
        for name, value in zip(names, self._data):
            value[1] = name
        return self._data

    def on_category_add_button_clicked(self,
                                       slot: Callable[[], Any]) -> None:
        "Обработать нажатие кнопки 'Добавить'"
        self.category_add_button.clicked.connect(slot)

    def on_category_delete_button_clicked(self,
                                          slot: Callable[[], Any]) -> None:
        "Обработать нажатие кнопки 'Удалить выбранную категорию'"
        self.category_delete_button.clicked.connect(slot)

    def on_category_save_changes_button_clicked(self,
                                                slot: Callable[[], Any]) -> None:
        "Обработать нажатие кнопки 'Сохранить изменения'"
        self.category_save_changes_button.clicked.connect(slot)
