import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=True, index=True)
