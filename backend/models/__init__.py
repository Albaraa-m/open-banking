from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # TODO There must be a better way to this

from models.bank_connection import BankConnection  # noqa
from models.user import User  # noqa

__all__ = ["User", "Base", "BankConnection"]
