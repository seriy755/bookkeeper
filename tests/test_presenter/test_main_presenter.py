"""
Тесты для модуля с общим представителем
"""
import pytest

from PySide6.QtWidgets import QErrorMessage

from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.repository.memory_repository import MemoryRepository

from bookkeeper.presenter.main_presenter import MainPresenter

from bookkeeper.view.main_window import MainWindow


@pytest.fixture
def view():
    return MainWindow()


def test_create_main_presenter(view):
    cat_repo = MemoryRepository[Category]()
    exp_repo = MemoryRepository[Expense]()
    budg_repo = MemoryRepository[Budget]()
    main_presenter = MainPresenter(view, exp_repo,
                                   cat_repo, budg_repo)
    assert main_presenter.view is not None


def test_show(qtbot, view):
    cat_repo = MemoryRepository[Category]()
    exp_repo = MemoryRepository[Expense]()
    budg_repo = MemoryRepository[Budget]()
    main_presenter = MainPresenter(view, exp_repo,
                                   cat_repo, budg_repo)
    assert main_presenter.show() is None


def test_set_data(view):
    cat_repo = MemoryRepository[Category]()
    exp_repo = MemoryRepository[Expense]()
    budg_repo = MemoryRepository[Budget]()
    c = Category(name='Продукты', parent=None)
    e = Expense(100, 1)
    cat_repo.add(c)
    exp_repo.add(e)
    main_presenter = MainPresenter(view, exp_repo,
                                   cat_repo, budg_repo)
    assert main_presenter.set_data() is None


def test_expense_add(qtbot, view, monkeypatch):
    cat_repo = MemoryRepository[Category]()
    exp_repo = MemoryRepository[Expense]()
    budg_repo = MemoryRepository[Budget]()
    main_presenter = MainPresenter(view, exp_repo,
                                   cat_repo, budg_repo)
    monkeypatch.setattr(QErrorMessage, 'exec',
                        lambda *args: QErrorMessage.done)
    assert main_presenter.handle_expense_add_button_clicked() is None
    assert len(main_presenter.exp_pres.data()) == 0

    c = Category(name='Продукты', parent=None)
    cat_repo.add(c)
    main_presenter = MainPresenter(view, exp_repo,
                                   cat_repo, budg_repo)
    main_presenter.set_data()

    assert main_presenter.handle_expense_add_button_clicked() is None
    assert len(main_presenter.exp_pres.data()) == 1

    main_presenter.view.amount_line_edit.setText('')
    assert main_presenter.handle_expense_add_button_clicked() is None


def test_expense_delete(view):
    cat_repo = MemoryRepository[Category]()
    exp_repo = MemoryRepository[Expense]()
    budg_repo = MemoryRepository[Budget]()
    main_presenter = MainPresenter(view, exp_repo,
                                   cat_repo, budg_repo)
    assert main_presenter.handle_expense_delete_button_clicked() is None

    c = Category(name='Продукты', parent=None)
    e = Expense(100, 1)
    cat_repo.add(c)
    exp_repo.add(e)
    main_presenter = MainPresenter(view, exp_repo,
                                   cat_repo, budg_repo)
    main_presenter.set_data()

    index = main_presenter.view.expense_grid.item_model.index(0, 0)
    main_presenter.view.expense_grid.setCurrentIndex(index)
    assert main_presenter.handle_expense_delete_button_clicked() is None
    assert len(main_presenter.exp_pres.data()) == 0


def test_expense_save_changes(qtbot, view, monkeypatch):
    cat_repo = MemoryRepository[Category]()
    exp_repo = MemoryRepository[Expense]()
    budg_repo = MemoryRepository[Budget]()
    c = Category(name='Продукты', parent=None)
    e = Expense(100, 1)
    cat_repo.add(c)
    exp_repo.add(e)
    main_presenter = MainPresenter(view, exp_repo,
                                   cat_repo, budg_repo)
    main_presenter.set_data()

    new_data = [[e.expense_date, 200, c.name, e.comment]]
    main_presenter.view.set_expense_grid(new_data, [e.pk])
    main_presenter.handle_expense_save_changes_button_clicked()
    assert main_presenter.exp_pres.data()[0][1] == 200

    monkeypatch.setattr(QErrorMessage, 'exec',
                        lambda *args: QErrorMessage.done)

    new_data = [[e.expense_date, -200, c.name, e.comment]]
    main_presenter.view.set_expense_grid(new_data, [e.pk])
    main_presenter.handle_expense_save_changes_button_clicked()
    assert main_presenter.exp_pres.data()[0][1] == 200

    new_data = [[e.expense_date, 'число', c.name, e.comment]]
    main_presenter.view.set_expense_grid(new_data, [e.pk])
    main_presenter.handle_expense_save_changes_button_clicked()
    assert main_presenter.exp_pres.data()[0][1] == 200

    new_data = [[e.expense_date, 200, 'Мясо', e.comment]]
    main_presenter.view.set_expense_grid(new_data, [e.pk])
    main_presenter.handle_expense_save_changes_button_clicked()
    assert main_presenter.exp_pres.data()[0][2] == 1

    new_data = [['202020', 200, c.name, e.comment]]
    main_presenter.view.set_expense_grid(new_data, [e.pk])
    main_presenter.handle_expense_save_changes_button_clicked()
    assert main_presenter.exp_pres.data()[0][0] == e.expense_date


def test_category_edit(qtbot, view):
    cat_repo = MemoryRepository[Category]()
    exp_repo = MemoryRepository[Expense]()
    budg_repo = MemoryRepository[Budget]()
    main_presenter = MainPresenter(view, exp_repo,
                                   cat_repo, budg_repo)
    assert main_presenter.handle_category_edit_button_clicked() is None


def test_category_add(qtbot, view, monkeypatch):
    cat_repo = MemoryRepository[Category]()
    exp_repo = MemoryRepository[Expense]()
    budg_repo = MemoryRepository[Budget]()
    main_presenter = MainPresenter(view, exp_repo,
                                   cat_repo, budg_repo)
    monkeypatch.setattr(QErrorMessage, 'exec',
                        lambda *args: QErrorMessage.done)
    assert main_presenter.handle_category_add_button_clicked() is None
    assert len(main_presenter.cat_pres.data()) == 0

    c = Category(name='Продукты', parent=None)
    cat_repo.add(c)
    main_presenter = MainPresenter(view, exp_repo,
                                   cat_repo, budg_repo)
    main_presenter.set_data()

    main_presenter.view.category_editor.new_category_line_edit.setText('Продукты')
    assert main_presenter.handle_category_add_button_clicked() is None
    assert len(main_presenter.cat_pres.data()) == 1

    main_presenter.view.category_editor.new_category_line_edit.setText('Мясо')
    assert main_presenter.handle_category_add_button_clicked() is None
    assert len(main_presenter.cat_pres.data()) == 2


def test_category_delete(view):
    cat_repo = MemoryRepository[Category]()
    exp_repo = MemoryRepository[Expense]()
    budg_repo = MemoryRepository[Budget]()
    main_presenter = MainPresenter(view, exp_repo,
                                   cat_repo, budg_repo)
    assert main_presenter.handle_category_delete_button_clicked() is None

    c = Category(name='Продукты', parent=None)
    e = Expense(100, 1)
    cat_repo.add(c)
    exp_repo.add(e)
    main_presenter = MainPresenter(view, exp_repo,
                                   cat_repo, budg_repo)
    main_presenter.set_data()
    main_presenter.view.category_editor.update_data([[1, 'Продукты', None]])

    index = main_presenter.view.category_editor.model.index(0, 0)
    main_presenter.view.category_editor.tree.setCurrentIndex(index)
    assert main_presenter.handle_category_delete_button_clicked() is None
    assert len(main_presenter.cat_pres.data()) == 0


def test_category_save_changes(qtbot, view, monkeypatch):
    cat_repo = MemoryRepository[Category]()
    exp_repo = MemoryRepository[Expense]()
    budg_repo = MemoryRepository[Budget]()
    c = Category(name='Продукты', parent=None)
    e = Expense(100, 1)
    cat_repo.add(c)
    exp_repo.add(e)
    main_presenter = MainPresenter(view, exp_repo,
                                   cat_repo, budg_repo)
    main_presenter.set_data()
    main_presenter.view.category_editor.update_data([[1, 'Продукты', None]])

    new_data = [[1, 'Мясо', None]]
    main_presenter.view.category_editor.update_data(new_data)
    main_presenter.handle_category_save_changes_button_clicked()
    assert main_presenter.cat_pres.data()[0][1] == 'Мясо'

    monkeypatch.setattr(QErrorMessage, 'exec',
                        lambda *args: QErrorMessage.done)

    new_data = [[1, ' ', None]]
    main_presenter.view.category_editor.update_data(new_data)
    main_presenter.handle_category_save_changes_button_clicked()
    assert main_presenter.cat_pres.data()[0][1] == 'Мясо'
