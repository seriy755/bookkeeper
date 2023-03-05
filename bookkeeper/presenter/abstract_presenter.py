"""
Модуль содержит описание абстрактного presenterа
"""

from abc import ABC, abstractmethod


class AbstractPresenter(ABC):
    """
    Абстрактный presenter.
    Абстрактные методы:
    data
    add_data
    """
    
    @abstractmethod
    def data(self) -> list[type]:
        pass
    
    @abstractmethod
    def add_data(self, **kwargs) -> None:
        pass
    