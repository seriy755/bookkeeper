"""
Тесты для модуля с представителем категорий
"""
import pytest

from bookkeeper.models.category import Category
from bookkeeper.repository.memory_repository import MemoryRepository

from bookkeeper.presenter.category_presenter import CategoryPresenter


@pytest.fixture
def repo():
    return MemoryRepository()


def test_create_category_presenter(repo):
    category_presenter = CategoryPresenter(repo)
    assert len(category_presenter._data) == 0


def test_add_data(repo):
    category_presenter = CategoryPresenter(repo)
    category_presenter.add_data('Продукты', None)
    assert len(category_presenter._data) == 1


def test_get_data(repo):
    category_presenter = CategoryPresenter(repo)
    category_presenter.add_data('Продукты', None)
    assert len(category_presenter.data()) == 1

    c = Category(name='Продукты', parent=None, pk=1)
    assert category_presenter.get(1) == c
    assert category_presenter.get_all() == [c]


def test_delete_data(repo):
    category_presenter = CategoryPresenter(repo)
    category_presenter.add_data('Продукты', None)
    category_presenter.add_data('Фрукты', 1)
    c = Category(name='Продукты', parent=None, pk=1)
    category_presenter.delete_data(c)
    assert len(category_presenter.data()) == 1


def test_update_data(repo):
    category_presenter = CategoryPresenter(repo)
    category_presenter.add_data('Продукты', None)
    c = Category(name='Мясо', parent=None, pk=1)
    category_presenter.update_data(c)
    assert category_presenter.get(1) == c
