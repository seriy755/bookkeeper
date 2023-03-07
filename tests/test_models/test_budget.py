"""
Тесты для модели бюджета
"""
from datetime import datetime

import pytest

from bookkeeper.models.budget import Budget
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.expense import Expense


@pytest.fixture
def repo():
    return MemoryRepository()


def test_create_object():
    b = Budget(amount=100, period='день', category=1, restrict=1000, pk=1)
    assert b.amount == 100
    assert b.category == 1
    assert b.restrict == 1000
    assert b.period == 'день'
    assert b.pk == 1
    
    b = Budget(100, 'месяц')
    assert b.amount == 100
    assert b.category == None
    assert b.restrict == None
    assert b.period == 'месяц'
    assert b.pk == 0
    

def test_reassign():
    """
    budget should not be frozen
    """
    b = Budget(100, 'день')
    b.period = 'месяц'
    b.pk = 1
    assert b.period == 'месяц'
    assert b.pk == 1


def test_eq():
    """
    budget should implement __eq__ method
    """
    b1 = Budget(amount=100, period='день', category=1)
    b2 = Budget(amount=100, period='день', category=1)
    assert b1 == b2   


def test_get_amounts(repo):
    e1 = Expense(100, 1)
    e2 = e = Expense(100, 1)
    repo.add(e1)
    repo.add(e2)
    amounts = [200, 200, 200]
    assert Budget.get_amounts(repo) == amounts
    

def test_create_from_restricts(repo):
    e1 = Expense(100, 1)
    e2 = e = Expense(100, 1)
    repo.add(e1)
    repo.add(e2)
    restricts = [(1, 1000), (None, 7000), (None, None)]
    b1 = Budget(200, 'день', 1, 1000)
    b2 = Budget(200, 'неделя', None, 7000)
    b3 = Budget(200, 'месяц', None, None)
    budgets = [b1, b2, b3]
    assert Budget.create_from_restricts(restricts, repo) == budgets
