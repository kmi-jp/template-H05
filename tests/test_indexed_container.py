import pytest

from data.index import Index
from data.indexed_container import IndexedContainer
from data.exceptions import IndexMismatchError


@pytest.fixture
def users():
    return Index(labels=["user 1", "user 2", "user 3", "user 4"], name="names")


@pytest.fixture
def numbers(users):
    return IndexedContainer([1, 2, 3, 4], index=users)


def test_values_property(numbers, users):
    assert numbers.values == [1, 2, 3, 4]
    with pytest.raises(AttributeError):
        numbers.values = []


def test_index_property(numbers, users):
    assert numbers.index == users
    
    with pytest.raises(IndexMismatchError):
        numbers.index = Index(labels=[42])
    
    new_index = Index(labels=['a', 'b', 'c', 'd'])
    numbers.index = new_index
    
    assert numbers.index == new_index