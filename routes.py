from flask import Blueprint, redirect, render_template, request, url_for

from ToDoItem import ItemStatus
from trello_client import Trello
from view_models import ItemsViewModel

bp = Blueprint("main", __name__, template_folder="templates")


@bp.route("/", methods=["GET"])
def index():
    item_view_model = ItemsViewModel(Trello().get_items())
    return render_template("index.html", view_model=item_view_model)


@bp.route("/", methods=["POST"])
def add():
    title = request.form.get("title")
    Trello().add_item(title=title)
    return redirect(url_for("main.index"))


@bp.route(
    "/items/<string:item_id>/to_do", methods=["POST"]
)  # Should be patch, but can't do without a forms library
def reset_item(item_id):
    Trello().update_status(item_id, ItemStatus.TO_DO)
    return redirect(url_for("main.index"))


@bp.route(
    "/items/<string:item_id>/do", methods=["POST"]
)  # Should be patch, but can't do without a forms library
def do_item(item_id):
    Trello().update_status(item_id, ItemStatus.DOING)
    return redirect(url_for("main.index"))


@bp.route(
    "/items/<string:item_id>/done", methods=["POST"]
)  # Should be patch, but can't do without a forms library
def complete_item(item_id):
    Trello().update_status(item_id, ItemStatus.DONE)
    return redirect(url_for("main.index"))
