from flask import Blueprint, redirect, render_template, request, url_for
from flask_login.utils import login_required

from app.mongo_client import MongoClient
from app.ToDoItem import ItemStatus
from app.view_models import ItemsViewModel

bp = Blueprint("main", __name__, template_folder="templates")


@bp.route("/", methods=["GET"])
@login_required
def index():
    item_view_model = ItemsViewModel(MongoClient().get_items())
    return render_template("index.html", view_model=item_view_model)


@login_required
@bp.route("/", methods=["POST"])
def add():
    title = request.form.get("title")
    MongoClient().add_item(title=title)
    return redirect(url_for("main.index"))


@bp.route(
    "/items/<string:item_id>/to_do", methods=["POST"]
)  # Should be patch, but can't do without a forms library
def reset_item(item_id):
    MongoClient().update_status(item_id, ItemStatus.TO_DO)
    return redirect(url_for("main.index"))


@bp.route(
    "/items/<string:item_id>/do", methods=["POST"]
)  # Should be patch, but can't do without a forms library
def do_item(item_id):
    MongoClient().update_status(item_id, ItemStatus.DOING)
    return redirect(url_for("main.index"))


@bp.route(
    "/items/<string:item_id>/done", methods=["POST"]
)  # Should be patch, but can't do without a forms library
def complete_item(item_id):
    MongoClient().update_status(item_id, ItemStatus.DONE)
    return redirect(url_for("main.index"))
