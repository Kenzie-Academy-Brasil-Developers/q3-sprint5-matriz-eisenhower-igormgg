from dataclasses import dataclass
from sqlalchemy import Column, Integer, String

from app.configs.database import db

@dataclass
class Eisenhowers_Model(db.Model):
    id: int
    type: str

    __tablename__ = "eisenhowers"

    id = Column(Integer, primary_key=True)
    type = Column(String(100))