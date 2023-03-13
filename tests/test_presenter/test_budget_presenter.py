"""
Тесты для модуля с представителем бюджета
"""
import pytest

from PySide6.QtWidgets import QErrorMessage

from bookkeeper.models.expense import Expense
from bookkeeper.repository.memory_repository import MemoryRepository

from bookkeeper.presenter.budget_presenter import BudgetPresenter


@pytest.fixture
def repo():
    return MemoryRepository()


def test_create_budget_presenter(repo):
    budget_presenter = BudgetPresenter(repo)
    assert budget_presenter._data is not None


def test_get_data(repo):
    budget_presenter = BudgetPresenter(repo)
    data = budget_presenter.data()
    assert len(data) == 3


def test_update_data(repo):
    budget_presenter = BudgetPresenter(repo)
    e = Expense(100, 1)
    exp_repo = MemoryRepository[Expense]()
    exp_repo.add(e)

    budget_presenter.update_data(exp_repo)
    data = budget_presenter.data()
    assert data[0][0] == 100
    assert data[1][0] == 100
    assert data[2][0] == 100


def test_update_restricts(qtbot, repo, monkeypatch):
    budget_presenter = BudgetPresenter(repo)
    restricts = ['100', '200', '300']

    budget_presenter.update_restricts(restricts)
    data = budget_presenter.data()
    assert data[0][1] == 100
    assert data[1][1] == 200
    assert data[2][1] == 300

    monkeypatch.setattr(QErrorMessage, 'exec',
                        lambda *args: QErrorMessage.done)
    restricts = ['-100', '250', 'abc']
    budget_presenter.update_restricts(restricts)
    data = budget_presenter.data()
    assert data[0][1] == 100
    assert data[1][1] == 250
    assert data[2][1] == 300
