import pytest

from data.index import Index


@pytest.fixture
def users():
    return Index(labels=["user 1", "user 2", "user 3", "user 4"], name="names")


def test_len(users):
    assert len(users) == 4


def test_labels_property(users):
    assert users.labels == ["user 1", "user 2", "user 3", "user 4"]
    with pytest.raises(AttributeError):
        users.labels = [] 
