from flask import current_app
import requests

from ToDoItem import ToDoItem

TRELLO_API_BASE_URL = "https://api.trello.com/1/"
TRELLO_BOARD_ID = "5eece6b3ad8029531e97e30f"
TRELLO_TODO_LIST_ID = "5eece6b3ad8029531e97e310"
TRELLO_DONE_LIST_ID = "5eece6b3ad8029531e97e312"


def get_auth_params():
    return {
        "key": current_app.config["TRELLO_API_KEY"],
        "token": current_app.config["TRELLO_API_TOKEN"],
    }


def get_item_from_trello_card(card_json):
    status = "To Do" if card_json["idList"] == TRELLO_TODO_LIST_ID else "Complete"
    return ToDoItem(id=card_json["id"], status=status, title=card_json["name"])


def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """

    r = requests.get(
        f"{TRELLO_API_BASE_URL}/boards/{TRELLO_BOARD_ID}/cards",
        params=get_auth_params(),
    )

    return [get_item_from_trello_card(item) for item in r.json()]


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    r = requests.get(f"{TRELLO_API_BASE_URL}/cards/{id}", params=get_auth_params())
    item = r.json()
    return get_item_from_trello_card(item)


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    r = requests.post(
        f"{TRELLO_API_BASE_URL}/cards",
        params={"name": title, "idList": TRELLO_TODO_LIST_ID, **get_auth_params()},
    )
    return get_item_from_trello_card(r.json())


def move_to_done(item_id):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item_id: The item_id to move to the done list.
    """
    r = requests.put(
        f"{TRELLO_API_BASE_URL}/cards/{item_id}",
        params={"idList": TRELLO_DONE_LIST_ID, **get_auth_params()},
    )
    return get_item_from_trello_card(r.json())
