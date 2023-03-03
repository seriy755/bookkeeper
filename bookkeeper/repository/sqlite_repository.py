"""
Модуль описывает репозиторий, работающий в СУБД SQlite
"""

import sqlite3 as sl
from typing import Any
from inspect import get_annotations

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SqliteRepository(AbstractRepository[T]):
    """
    Репозиторий, работающий с СУБД SQlite.
    """

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.cls = cls
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        
    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sl.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES({p})',
                    values
            )
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        pass

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        pass

    def update(self, obj: T) -> None:
        pass

    def delete(self, pk: int) -> None:
        pass
