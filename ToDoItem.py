from dataclasses import dataclass


@dataclass
class ToDoItem:
    id: int
    status: str
    title: str
