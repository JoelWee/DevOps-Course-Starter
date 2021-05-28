from datetime import datetime

from bson.objectid import ObjectId
from flask import current_app

from app.ToDoItem import ItemStatus, ToDoItem


class MongoClient:
    def __init__(self):
        self.todo_col = current_app.mongo.db.todos

    def get_item_from_json(self, json) -> ToDoItem:
        return ToDoItem(
            id=str(json["_id"]),
            status=ItemStatus(json["status"]),
            title=json["title"],
            last_modified=json["last_modified"],
        )

    def get_items(self):
        """
        Fetches all saved items from the session.

        Returns:
            list: The list of saved items.
        """
        items = self.todo_col.find()

        return [self.get_item_from_json(item) for item in items]

    def get_item(self, item_id: str):
        """
        Fetches the saved item with the specified ID.

        Args:
            id: The ID of the item.

        Returns:
            item: The saved item, or None if no items match the specified ID.
        """
        item = self.todo_col.find_one({"_id": ObjectId(item_id)})
        return self.get_item_from_json(item)

    def add_item(self, title):
        """
        Adds a new item with the specified title to the session.

        Args:
            title: The title of the item.

        Returns:
            None
        """
        current_app.logger.info("TODO item '%s' added", title)
        self.todo_col.insert_one(
            {
                "title": title,
                "status": ItemStatus.TO_DO.value,
                "last_modified": datetime.utcnow(),
            }
        )

    def update_status(self, item_id: str, status: ItemStatus):
        """
        Updates an existing item in the session. Ignore if no existing item matches the ID of the specified item.

        Args:
            item_id: The item_id to move to the done list.
        """
        current_app.logger.info(
            "TODO item '%s' updated to %s", item_id, status.value)
        self.todo_col.update_one(
            {
                "_id": ObjectId(item_id),
            },
            {
                "$set": {"status": status.value},
                "$currentDate": {"last_modified": True},
            },
        )
