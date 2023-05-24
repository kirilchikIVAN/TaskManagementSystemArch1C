import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from db import field_constraints
from db.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=True, index=True)
    name = sa.Column(
        sa.String(field_constraints.DEFAULT_STRING_LENGTH),
        nullable=False,
        comment="User name",
    )
    boss_id = mapped_column(ForeignKey("users.id"))
    boss = relationship("User", remote_side=[id])
