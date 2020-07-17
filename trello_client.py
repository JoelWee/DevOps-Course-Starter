from flask import current_app
import requests
from ToDoItem import ToDoItem

TRELLO_API_BASE_URL = "https://api.trello.com/1/"
TRELLO_TODO_LIST_ID = "5eece6b3ad8029531e97e310"
TRELLO_DONE_LIST_ID = "5eece6b3ad8029531e97e312"


class Trello:
    def __init__(self):
        self.key = current_app.config["TRELLO_API_KEY"]
        self.token = current_app.config["TRELLO_API_TOKEN"]
        self.auth_params = {
            "key": self.key,
            "token": self.token,
        }
        self.board_id = current_app.config["TRELLO_BOARD_ID"]

    @staticmethod
    def get_item_from_trello_card(card_json) -> ToDoItem:
        status = "To Do" if card_json["idList"] == TRELLO_TODO_LIST_ID else "Complete"
        return ToDoItem(id=card_json["id"], status=status, title=card_json["name"])

    def get_items(self):
        """
        Fetches all saved items from the session.

        Returns:
            list: The list of saved items.
        """
        r = requests.get(
            f"{TRELLO_API_BASE_URL}/boards/{self.board_id}/cards",
            params=self.auth_params,
        )
        return [self.get_item_from_trello_card(item) for item in r.json()]

    def get_item(self, id):
        """
        Fetches the saved item with the specified ID.

        Args:
            id: The ID of the item.

        Returns:
            item: The saved item, or None if no items match the specified ID.
        """
        r = requests.get(f"{TRELLO_API_BASE_URL}/cards/{id}", params=self.auth_params)
        item = r.json()
        return self.get_item_from_trello_card(item)

    def add_item(self, title):
        """
        Adds a new item with the specified title to the session.

        Args:
            title: The title of the item.

        Returns:
            item: The saved item.
        """
        r = requests.post(
            f"{TRELLO_API_BASE_URL}/cards",
            params={"name": title, "idList": TRELLO_TODO_LIST_ID, **self.auth_params},
        )
        return self.get_item_from_trello_card(r.json())

    def move_to_done(self, item_id):
        """
        Updates an existing item in the session. Ignore if no existing item matches the ID of the specified item.

        Args:
            item_id: The item_id to move to the done list.
        """
        r = requests.put(
            f"{TRELLO_API_BASE_URL}/cards/{item_id}",
            params={"idList": TRELLO_DONE_LIST_ID, **self.auth_params},
        )
        return self.get_item_from_trello_card(r.json())
