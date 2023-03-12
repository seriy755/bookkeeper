"""
Модуль для запуска приложения
"""
import sys
from PySide6.QtWidgets import QApplication

from bookkeeper.view.main_window import MainWindow
from bookkeeper.view.modal_windows import file_dialog

from bookkeeper.presenter.main_presenter import MainPresenter

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SqliteRepository


if __name__ == '__main__':
    app = QApplication(sys.argv)

    db_name = file_dialog()
    if db_name:

        view = MainWindow()

        cat_repo = SqliteRepository[Category](db_name, Category)
        budg_repo = SqliteRepository[Budget](db_name, Budget)
        exp_repo = SqliteRepository[Expense](db_name, Expense)

        window = MainPresenter(view, exp_repo, cat_repo, budg_repo)
        window.show()
        sys.exit(app.exec())
