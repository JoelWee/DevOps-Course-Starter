from datetime import datetime

import requests
from flask import current_app

from app.ToDoItem import ItemStatus, ToDoItem

TRELLO_API_BASE_URL = "https://api.trello.com/1"


class Trello:
    def __init__(self):
        self.key = current_app.config["TRELLO_API_KEY"]
        self.token = current_app.config["TRELLO_API_TOKEN"]
        self.auth_params = {
            "key": self.key,
            "token": self.token,
        }
        self.board_id = current_app.config["TRELLO_BOARD_ID"]
        self.lists = TrelloLists(
            requests.get(
                f"{TRELLO_API_BASE_URL}/boards/{self.board_id}/lists",
                params=self.auth_params,
            ).json()
        )

    def get_item_from_trello_card(self, card_json) -> ToDoItem:
        return ToDoItem(
            id=card_json["id"],
            status=ItemStatus(self.lists.get_name(card_json["idList"])),
            title=card_json["name"],
            last_modified=datetime.strptime(
                card_json["dateLastActivity"], "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
        )

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

    def get_item(self, item_id):
        """
        Fetches the saved item with the specified ID.

        Args:
            id: The ID of the item.

        Returns:
            item: The saved item, or None if no items match the specified ID.
        """
        r = requests.get(
            f"{TRELLO_API_BASE_URL}/cards/{item_id}", params=self.auth_params
        )
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
            params={
                "name": title,
                "idList": self.lists.get_id(ItemStatus.TO_DO.value),
                **self.auth_params,
            },
        )
        return self.get_item_from_trello_card(r.json())

    def update_status(self, item_id, status: ItemStatus):
        """
        Updates an existing item in the session. Ignore if no existing item matches the ID of the specified item.

        Args:
            item_id: The item_id to move to the done list.
        """
        r = requests.put(
            f"{TRELLO_API_BASE_URL}/cards/{item_id}",
            params={"idList": self.lists.get_id(status.value), **self.auth_params},
        )
        return self.get_item_from_trello_card(r.json())


class TrelloLists:
    def __init__(self, lists_json):
        self.name_to_id = {
            list_json["name"]: list_json["id"] for list_json in lists_json
        }
        self.id_to_name = {
            list_json["id"]: list_json["name"] for list_json in lists_json
        }

    def get_id(self, name: str):
        return self.name_to_id[name]

    def get_name(self, list_id: str):
        return self.id_to_name[list_id]


class TrelloBoard:
    def __init__(self, key, token):
        self.key = key
        self.token = token
        self.auth_params = {
            "key": self.key,
            "token": self.token,
        }

    def create(self, name: str) -> str:
        return requests.post(
            f"{TRELLO_API_BASE_URL}/boards", params={"name": name, **self.auth_params}
        ).json()["id"]

    def delete(self, id: str):
        return requests.delete(
            f"{TRELLO_API_BASE_URL}/boards/{id}", params=self.auth_params
        ).json()
