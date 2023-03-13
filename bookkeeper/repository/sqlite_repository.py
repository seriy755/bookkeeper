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
        with sl.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} \
                ({', '.join(self.fields.keys())})")
        con.close()

    def _row_to_cls(self, pk: int, row: tuple[Any]) -> T:
        "Функция для конвертации строки БД в объект типа T"
        attrs = {}
        for field, value in zip(self.fields, row):
            attrs[field] = value
        obj = self.cls(**attrs)
        obj.pk = pk
        return obj  # type: ignore

    def add(self, obj: T) -> int:
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        names = ', '.join(self.fields.keys())
        question = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sl.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES({question})',
                values
            )
            obj.pk = cur.lastrowid  # type: ignore
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        with sl.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {self.table_name} WHERE ROWID == {pk}")
            row = cur.fetchone()
        con.close()
        if row is None:
            return None
        return self._row_to_cls(pk, row)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        with sl.connect(self.db_file) as con:
            cur = con.cursor()
            if where is None:
                cur.execute(f"SELECT ROWID, * FROM {self.table_name}")
                rows = cur.fetchall()
            else:
                fields = " AND ".join(f"{x}=?" for x in where.keys())
                fields = fields.replace("pk", "ROWID")
                conds = list(where.values())
                cur.execute(f"SELECT ROWID, * FROM {self.table_name} WHERE {fields}",
                            conds)
                rows = cur.fetchall()
        con.close()
        return [self._row_to_cls(row[0], row[1:]) for row in rows]

    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        with sl.connect(self.db_file) as con:
            cur = con.cursor()
            fields = ', '.join(f"{x}=?" for x in self.fields.keys())
            values = [getattr(obj, x) for x in self.fields]
            cur.execute(f"UPDATE {self.table_name} SET {fields} WHERE ROWID == {obj.pk}",
                        values)
        con.close()

    def delete(self, pk: int) -> None:
        with sl.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM {self.table_name} WHERE ROWID = {pk}")
            rowcount = cur.rowcount
        con.close()
        if rowcount == 0:
            raise KeyError('attempt to delete object with unknown primary key')

    def delete_all(self) -> None:
        " Функция для удаления всех записей из БД"
        with sl.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM {self.table_name}")
        con.close()
