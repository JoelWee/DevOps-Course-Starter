from datetime import datetime

import pytest

from ToDoItem import ItemStatus, ToDoItem
from view_models.items import ItemsViewModel

test_date = datetime(2020, 1, 1)


@pytest.fixture
def items_view_model():
    return ItemsViewModel(
        [
            ToDoItem("a", ItemStatus.TO_DO, "a", datetime.now()),
            ToDoItem("b", ItemStatus.TO_DO, "b", test_date),
            ToDoItem("c", ItemStatus.DOING, "c", datetime.now()),
            ToDoItem("d", ItemStatus.DONE, "d", test_date),
            ToDoItem("e", ItemStatus.DONE, "e", datetime.now()),
        ],
    )


def test_to_do_items(items_view_model):
    assert all(item.id in ("a", "b") for item in items_view_model.to_do_items)


def test_doing_items(items_view_model):
    assert all(item.id == "c" for item in items_view_model.doing_items)


def test_done_items(items_view_model):
    assert all(item.id in ("d", "e") for item in items_view_model.done_items)


def test_show_all_done_items_if_less_than_five(items_view_model):
    assert items_view_model.show_all_done_items


def test_do_not_show_all_done_items_if_at_least_five():
    items_view_model = ItemsViewModel(
        [
            ToDoItem("e", ItemStatus.DONE, "e", test_date),
            ToDoItem("f", ItemStatus.DONE, "f", test_date),
            ToDoItem("g", ItemStatus.DONE, "g", datetime.now()),
            ToDoItem("h", ItemStatus.DONE, "h", test_date),
            ToDoItem("i", ItemStatus.DONE, "i", test_date),
        ],
    )
    assert not items_view_model.show_all_done_items


def test_recent_done_items(items_view_model):
    assert all(item.id == "e" for item in items_view_model.recent_done_items)


def test_older_done_items(items_view_model):
    assert all(item.id == "d" for item in items_view_model.older_done_items)
