from sqlalchemy import Column, Integer, String

from models import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    customer_id = Column(String, nullable=True)
