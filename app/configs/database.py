from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app: Flask):
    db.init_app(app)
    app.db = db

    from app.models.tasks_model import Tasks_Model
    from app.models.eisenhowers_model import Eisenhowers_Model
    from app.models.tasks_categories_model import tasks_categories
    from app.models.categories_model import Categories_Model