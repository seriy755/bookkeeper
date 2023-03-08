"""
Модуль для описания графического интерфейса окна редактирования списка категорий
"""
from typing import Any

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import QModelIndex
from PySide6.QtWidgets import (QVBoxLayout, QWidget, QGridLayout,
                               QTreeView, QPushButton, QLineEdit,
                               QComboBox, QAbstractItemView,
                               QTreeWidgetItemIterator)


class CategoryEditorWindow(QWidget):
    "Класс для окна редактирования списка категорий"
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tree = QTreeView(self,
            selectionMode=QAbstractItemView.SingleSelection)
        self.layout.addWidget(self.tree)

        self.bottom_controls = QGridLayout()
        self.model = QStandardItemModel()
        self.root = self.model.invisibleRootItem()

        self.new_category_line_edit = QLineEdit()
        self.new_category_line_edit.setPlaceholderText('Новая категория')
        self.bottom_controls.addWidget(self.new_category_line_edit, 0, 0)

        self.category_dropdown = QComboBox()
        self.bottom_controls.addWidget(self.category_dropdown, 1, 0)

        self.category_add_button = QPushButton('Добавить')
        self.bottom_controls.addWidget(self.category_add_button, 2, 0)
        self.category_delete_button = QPushButton('Удалить выбранную категорию')
        self.bottom_controls.addWidget(self.category_delete_button, 3, 0)
        self.category_save_changes_button = QPushButton('Сохранить изменения')
        self.bottom_controls.addWidget(self.category_save_changes_button, 4, 0)

        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)
        self.layout.addWidget(self.bottom_widget)

    def init_model(self) -> None:
        "Инициализировать модель"
        self.model.clear()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Категория'])
        self.root = self.model.invisibleRootItem()
        self.tree.setModel(self.model)
        self.tree.expandAll()

    def update_data(self,
                    data: list[list[Any]]) -> None:
        "Обновить данные о списке категорий в модели"
        seen: dict[int, QStandardItem] = {}
        self.init_model()
        self._data = self.sort_data(data)
        for value in self._data:
            pk, name, parent = value

            if parent is None:
                parent = self.root
            else:
                parent = seen[parent]
            
            parent.appendRow([
                QStandardItem(name)])
            seen[pk] = parent.child(parent.rowCount() - 1)
        self.set_category_dropdown()
        
    def sort_data(self, data, parent=None):
        new_data: list[list[Any]] = []
        for value in data:
            pk, name, pid = value
            if pid == parent:
                new_data.append([pk, name, pid])
                new_data += self.sort_data(data, pk)
        return new_data

    def set_category_dropdown(self) -> None:
        "Обновить данные о списке категорий во всплывающем списке"
        self.category_dropdown.clear()
        self.category_dropdown.addItem('')
        for value in self._data:
            self.category_dropdown.addItem(value[1], value[0])

    def get_new_category(self) -> str:
        "Получить имя новой категории"
        return str(self.new_category_line_edit.text())

    def get_selected_parent(self) -> int | None:
        "Получить имя родительской категории для новой категории"
        return self.category_dropdown.itemData(
            self.category_dropdown.currentIndex())

    def get_selected_category(self) -> str:
        "Получить имя выбранной в модели категории"
        return str(self.tree.selectedIndexes()[0].data())
    
    def get_all_names(self,
                      parent = QModelIndex()) -> list[list[Any]]:
        "Получить все имена из модели категорий"
        names: list[str] = []
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

    def on_category_add_button_clicked(self, slot: type) -> None:
        "Обработать нажатие кнопки 'Добавить'"
        self.category_add_button.clicked.connect(slot)

    def on_category_delete_button_clicked(self, slot: type) -> None:
        "Обработать нажатие кнопки 'Удалить выбранную категорию'"
        self.category_delete_button.clicked.connect(slot)
        
    def on_category_save_changes_button_clicked(self, slot: type) -> None:
        "Обработать нажатие кнопки 'Сохранить изменения'"
        self.category_save_changes_button.clicked.connect(slot)
