from bookkeeper.view.main_window import MainWindow
from bookkeeper.presenter.main_presenter import MainPresenter
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SqliteRepository
import sys
from PySide6.QtWidgets import QApplication

DB_NAME = 'databases/simple_sqlite_client.db'

if __name__ == '__main__':
    app = QApplication(sys.argv)

    view = MainWindow()
    model = None

    cat_repo = SqliteRepository[Category](DB_NAME, Category)
    exp_repo = SqliteRepository[Expense](DB_NAME, Expense)

    window = MainPresenter(view, exp_repo, cat_repo)
    window.show()
    sys.exit(app.exec())