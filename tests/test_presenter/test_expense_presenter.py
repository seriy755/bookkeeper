"""
Тесты для модуля с представителем расходов
"""
import pytest

from bookkeeper.models.expense import Expense
from bookkeeper.repository.memory_repository import MemoryRepository

from bookkeeper.presenter.expense_presenter import ExpensePresenter


@pytest.fixture
def repo():
    return MemoryRepository()


def test_create_expense_presenter(repo):
    expense_presenter = ExpensePresenter(repo)
    assert len(expense_presenter._data) == 0


def test_add_data(repo):
    expense_presenter = ExpensePresenter(repo)
    expense_presenter.add_data(100, 1)
    assert len(expense_presenter._data) == 1


def test_get_data(repo):
    expense_presenter = ExpensePresenter(repo)
    expense_presenter.add_data(100, 1)
    assert len(expense_presenter.data()) == 1
    assert expense_presenter.get_all_pk() == [1]

    e = Expense(amount=100, category=1, pk=1)
    assert expense_presenter.get(1) == e
    assert expense_presenter.get_all() == [e]


def test_delete_data(repo):
    expense_presenter = ExpensePresenter(repo)
    expense_presenter.add_data(100, 1)
    e = Expense(amount=100, category=1, pk=1)
    expense_presenter.delete_data(e)
    assert len(expense_presenter.data()) == 0


def test_update_data(repo):
    expense_presenter = ExpensePresenter(repo)
    expense_presenter.add_data(100, 1)
    e = Expense(amount=1000, category=1, pk=1)
    expense_presenter.update_data(e)
    assert expense_presenter.get(1) == e
