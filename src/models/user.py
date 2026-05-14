from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    full_name = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)

    is_active = Column(Boolean, default=True)

    products = relationship(
        "Product",
        back_populates="owner",
        cascade="all, delete"
    )