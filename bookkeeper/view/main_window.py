"""
Модуль для описания графического интерфейса
главного окна приложения. Вывод на экран
таблиц расходов, бюджета, списка категорий
элементов ввода и редактирования таблиц:
поле ввода суммы расхода
кнопка редактирования категорий
кнопка добаления расхода
кнопка удаления расхода
кнопка сохранения изменений
"""
# pylint: disable = no-name-in-module
# pylint: disable = too-many-instance-attributes
# mypy: disable-error-code="attr-defined,union-attr,assignment,arg-type"
from typing import Callable, Any

from PySide6.QtWidgets import (QVBoxLayout, QLabel,
                               QWidget, QGridLayout,
                               QComboBox, QLineEdit,
                               QPushButton, QMainWindow)

from bookkeeper.view.expense_view import ExpenseTableView
from bookkeeper.view.budget_view import BudgetTableView
from bookkeeper.view.category_view import CategoryEditorWindow


class MainWindow(QMainWindow):
    "Главное окно приложения"
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("The Bookkeeper App")
        self.resize(480, 640)

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel('Последние расходы'))
        self.expense_grid = ExpenseTableView()
        self.layout.addWidget(self.expense_grid)

        self.layout.addWidget(QLabel('Бюджет'))
        self.budget_grid = BudgetTableView()
        self.layout.addWidget(self.budget_grid)

        bottom_controls = QGridLayout()

        bottom_controls.addWidget(QLabel('Сумма'), 0, 0)

        self.amount_line_edit = QLineEdit('0')

        bottom_controls.addWidget(self.amount_line_edit, 0, 1)
        bottom_controls.addWidget(QLabel('Категория'), 1, 0)

        self.category_dropdown = QComboBox()

        bottom_controls.addWidget(self.category_dropdown, 1, 1)

        self.category_edit_button = QPushButton('Редактировать')
        bottom_controls.addWidget(self.category_edit_button, 1, 2)

        self.category_editor = CategoryEditorWindow()
        self.category_editor.setWindowTitle("Редактирование категорий")
        self.category_editor.resize(480, 640)

        self.expense_add_button = QPushButton('Добавить')
        bottom_controls.addWidget(self.expense_add_button, 2, 1)

        self.expense_delete_button = QPushButton('Удалить выбранные записи')
        bottom_controls.addWidget(self.expense_delete_button, 3, 1)

        self.expense_save_changes_button = QPushButton('Сохранить изменения')
        bottom_controls.addWidget(self.expense_save_changes_button, 4, 1)

        bottom_widget = QWidget()
        bottom_widget.setLayout(bottom_controls)

        self.layout.addWidget(bottom_widget)

        widget = QWidget()
        widget.setLayout(self.layout)

        self.setCentralWidget(widget)

    def set_expense_grid(self,
                         data: list[list[Any]],
                         ids: list[int]) -> None:
        "Вывести на экран таблицу расходов"
        self.expense_grid.set_expense_table(data, ids)

    def set_budget_grid(self,
                        data: list[list[Any]],
                        update: bool = False) -> None:
        "Вывести на экран таблицу бюджета"
        self.budget_grid.set_budget_table(data, update)

    def set_category_dropdown(self,
                              data: list[Any]) -> None:
        "Вывести на экран список категорий"
        self.category_dropdown.clear()
        for tup in data:
            self.category_dropdown.addItem(tup[1], tup[0])

    def get_selected_expense(self) -> set[int]:
        "Получить выделенную строку расхода"
        return self.expense_grid.get_selected_expense()

    def get_all_expenses(self) -> list[list[Any]]:
        "Получить все записи о расходах"
        return self.expense_grid.get_all_expenses()

    def get_all_restricts(self) -> list[str]:
        "Получить все записи об ограничениях бюджета"
        return self.budget_grid.get_all_restricts()

    def get_amount(self) -> str:
        "Получить введённую сумму"
        return self.amount_line_edit.text()

    def get_selected_cat(self) -> Any:
        "Получить выбранную категорию"
        return self.category_dropdown.itemData(
            self.category_dropdown.currentIndex())

    def show_category_editor_window(self,
                                    data: list[list[Any]]) -> None:
        "Открыть окно редактирования категорий"
        self.category_editor.update_data(data)
        self.category_editor.show()

    def on_expense_add_button_clicked(self,
                                      slot: Callable[[], Any]) -> None:
        "Обработать нажатие 'Добавить'"
        self.expense_add_button.clicked.connect(slot)

    def on_category_edit_button_clicked(self,
                                        slot: Callable[[], Any]) -> None:
        "Обработать нажатие кнопки 'Редактировать'"
        self.category_edit_button.clicked.connect(slot)

    def on_expense_delete_button_clicked(self,
                                         slot: Callable[[], Any]) -> None:
        "Обработать нажатие кнопки 'Удалить выбранную запись'"
        self.expense_delete_button.clicked.connect(slot)

    def on_expense_save_changes_button_clicked(self,
                                               slot: Callable[[], Any]) -> None:
        "Обработать нажатие кнопки 'Сохранить изменения'"
        self.expense_save_changes_button.clicked.connect(slot)
