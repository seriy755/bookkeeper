"""
Модуль для описания графического интерфейса главного окна приложения
"""

import sys
from PySide6.QtWidgets import (QVBoxLayout, QLabel, QWidget, QGridLayout, 
                               QComboBox, QLineEdit, QPushButton)
from PySide6 import QtCore, QtWidgets

from datetime import datetime

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SqliteRepository
from bookkeeper.view.expense_view import ExpenseTableView
from bookkeeper.view.budget_view import BudgetTableView


class MainWindow(QtWidgets.QMainWindow):
    "Главное окно приложения"
    def __init__(self):
        super().__init__()
        
        self.item_model = None
        self.setWindowTitle("The Bookkeeper App")
        self.resize(480, 640)

        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel('Последние расходы'))
        self.expense_grid = ExpenseTableView()
        self.layout.addWidget(self.expense_grid)

        self.layout.addWidget(QLabel('Бюджет'))
        self.budget_grid = BudgetTableView()
        self.layout.addWidget(self.budget_grid)

        self.bottom_controls = QGridLayout()

        self.bottom_controls.addWidget(QLabel('Сумма'), 0, 0)

        self.amount_line_edit = QLineEdit('0')

        self.bottom_controls.addWidget(self.amount_line_edit, 0, 1)
        self.bottom_controls.addWidget(QLabel('Категория'), 1, 0)

        self.category_dropdown = QComboBox()

        self.bottom_controls.addWidget(self.category_dropdown, 1, 1)

        self.category_edit_button = QPushButton('Редактировать')
        self.bottom_controls.addWidget(self.category_edit_button, 1, 2)

        self.expense_add_button = QPushButton('Добавить')
        self.bottom_controls.addWidget(self.expense_add_button, 2, 1)

        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)

        self.layout.addWidget(self.bottom_widget)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)
        
    def set_expense_grid(self, data):
        self.expense_grid.set_expense_table(data)
        
    def set_budget_grid(self, data):
        self.budget_grid.set_budget_table(data)
    
    def get_amount(self) -> float:
        return float(self.amount_line_edit.text())
    
    def get_selected_cat(self) -> int:
        return self.category_dropdown.itemData(
            self.category_dropdown.currentIndex()) 
    
    def set_category_dropdown(self, data):
        self.category_dropdown.clear()
        for tup in data:
            self.category_dropdown.addItem(tup[1], tup[0])
            
    def on_expense_add_button_clicked(self, slot):
        self.expense_add_button.clicked.connect(slot)
   
        
DB_FILE = 'databases/simple_sqlite_client.db'
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    cat_repo = SqliteRepository[Category](DB_FILE, Category)
    exp_repo = SqliteRepository[Expense](DB_FILE, Expense)

    window = MainWindow()
    exp_data = [
            [datetime(2023, 3, 4), 150, 'Чай', ''],
            [datetime(2023, 3, 4), 353.555, 'Кофе', ''],
            [datetime(2023, 3, 4), 123, 'Сыр', ''],
            [datetime(2023, 3, 4), 266, 'Колбаса', '']
        ]
    window.set_expense_grid(exp_data)
    
    bdgt_data = [
            [769, 1000],
            [6500, 7000],
            [24980.25, 30000]
        ]
    window.set_budget_grid(bdgt_data)
    
    cat_data = [
            [1, 'Продукты', None],
            [2, 'Сыр', 1],
            [3, 'Мясо', 1],
            [4, 'Книги', None]
        ]
    window.set_category_dropdown(cat_data)
    
    window.show()
    sys.exit(app.exec())