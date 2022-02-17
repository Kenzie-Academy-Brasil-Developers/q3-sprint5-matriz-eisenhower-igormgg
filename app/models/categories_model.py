from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Text

from app.configs.database import db

@dataclass
class Categories_Model(db.Model):
    id: int
    name: str
    description: str

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)