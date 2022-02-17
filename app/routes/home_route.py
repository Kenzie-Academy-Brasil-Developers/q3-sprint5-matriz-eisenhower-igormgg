from flask import Blueprint

from app.controllers.categories_controller import list_categories_tasks

bp_home = Blueprint("bp_home", __name__, url_prefix="/")

bp_home.get('')(list_categories_tasks)