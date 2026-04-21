from sqlalchemy import Column, Integer, String, TIMESTAMP
from datetime import datetime
from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True)
    password = Column(String, nullable=False)
    nickname = Column(String, unique=True, nullable=False)
