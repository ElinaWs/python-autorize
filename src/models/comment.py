from sqlalchemy import Column, Integer, String, ForeignKey
from src.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    review = Column(Integer) 
    text_of_comment = Column(String)
