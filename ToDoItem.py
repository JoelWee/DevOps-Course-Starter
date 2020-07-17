from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ItemStatus(Enum):
    TO_DO = "To Do"
    DOING = "Doing"
    DONE = "Done"


@dataclass(frozen=True)
class ToDoItem:
    id: str
    status: ItemStatus
    title: str
    last_modified: datetime
