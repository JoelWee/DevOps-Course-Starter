from datetime import datetime, timedelta
from typing import List

from ToDoItem import ItemStatus, ToDoItem


class ItemsViewModel:
    def __init__(self, items: List[ToDoItem]):
        self._items: List[ToDoItem] = items

    @property
    def items(self):
        return self._items

    @property
    def to_do_items(self):
        return [item for item in self._items if item.status == ItemStatus.TO_DO]

    @property
    def doing_items(self):
        return [item for item in self._items if item.status == ItemStatus.DOING]

    @property
    def done_items(self):
        return [item for item in self._items if item.status == ItemStatus.DONE]

    @property
    def show_all_done_items(self):
        return sum(1 for item in self._items if item.status == ItemStatus.DONE) < 5

    @property
    def recent_done_items(self):
        return [
            item
            for item in self.done_items
            if item.last_modified > datetime.now() - timedelta(days=1)
        ]

    @property
    def older_done_items(self):
        return list(set(self.done_items) - set(self.recent_done_items))
