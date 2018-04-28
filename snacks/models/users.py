from sqlalchemy import Column, Integer, String

from snacks.db import Base


class User(Base):
    """
    Data model for storing user info.

    Columns:
        - id: Integer
        - username: username
        - password_hash: hash of password with secret key
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
