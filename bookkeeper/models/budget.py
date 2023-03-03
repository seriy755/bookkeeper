"""
Модель бюджета
"""

from dataclasses import dataclass


@dataclass
class Budget:
    """
    Бюджет.
    period- срок
    category - id категории расходов
    amount - сумма
    pk - id записи в базе данных
    """
    period: int
    category: int
    amount: int
    pk: int = 0
