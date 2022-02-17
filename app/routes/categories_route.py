from flask import Blueprint

from app.controllers.categories_controller import create_category, delete_category, patch_category

bp_categories = Blueprint("bp_categories", __name__, url_prefix="/categories")

bp_categories.post('')(create_category)
bp_categories.patch('/<int:id>')(patch_category)
bp_categories.delete('/<int:id>')(delete_category)
