"""
Модуль содержит описание абстрактного presenterа
"""

from abc import ABC, abstractmethod


class AbstractPresenter(ABC):
    """
    Абстрактный presenter.
    Абстрактные методы:
    data
    """

    @abstractmethod
    def data(self) -> list[type]:
        "Получить данные из репозитория"
        pass
