"""
Модуль для описания представителя бюджета
"""
from typing import Any

from bookkeeper.models.category import Category
from bookkeeper.repository.abstract_repository import AbstractRepository


class CategoryPresenter():
    "Класс представителя категорий"
    def __init__(self,
                 repo: AbstractRepository['Category']) -> None:
        self.repo = repo
        self._data = self.repo.get_all()

    def data(self) -> list[list[Any]]:
        "Вернуть данные из репозитория в формате списка"
        data: list[list[Any]] = []
        for item in self._data:
            pk, name, parent = item.pk, item.name, item.parent
            data.append([pk, name, parent])
        return data

    def add_data(self, name: str,
                 parent: int | None) -> None:
        "Добавить данные в репозиторий"
        cat = Category(name=name, parent=parent)
        self.repo.add(cat)
        self._data = self.repo.get_all()

    def delete_data(self, cat: Category) -> None:
        "Удалить данные из репозитория"
        for child in cat.get_subcategories(self.repo):
            child.parent = cat.parent
            self.repo.update(child)
        self.repo.delete(cat.pk)
        self._data = self.repo.get_all()

    def update_data(self, cat: Category) -> None:
        "Обновить данные в репозитории"
        self.repo.update(cat)
        self._data = self.repo.get_all()

    def get(self, pk: int) -> Category | None:
        "получить объект из репозитория по его pk"
        return self.repo.get(pk)

    def get_all(self,
                where: dict[str, Any] | None = None) -> list['Category']:
        "Получить все записи из репозитория по некоторому условию"
        return self.repo.get_all(where)
