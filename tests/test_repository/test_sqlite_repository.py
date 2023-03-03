from bookkeeper.repository.sqlite_repository import SqliteRepository
from dataclasses import dataclass

import pytest

DB_FILE = "databases/test_sqlrepo.db"


@pytest.fixture
def custom_class():
    @dataclass
    class Custom():
        pk: int = 0

    return Custom


@pytest.fixture
def repo(custom_class, db_file=DB_FILE):
    return SqliteRepository(db_file, custom_class)


def test_crud(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    repo.delete(pk)
    assert repo.get(pk) is None
