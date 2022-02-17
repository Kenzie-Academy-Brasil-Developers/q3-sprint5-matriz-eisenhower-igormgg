from dataclasses import dataclass
from sqlalchemy import Column, ForeignKey, Integer, String, Text

from app.configs.database import db
from app.models.tasks_categories_model import tasks_categories

@dataclass
class Tasks_Model(db.Model):
    id: int
    name: str
    description: str
    duration: str
    categories: list

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    duration = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)

    eisenhowers_id = Column(Integer, ForeignKey('eisenhowers.id'))

    categories = db.relationship(
      "Categories_Model",
      secondary=tasks_categories,
      backref="tasks"
    )

    classification = db.relationship(
      "Eisenhowers_Model",
      backref="tasks"
    )