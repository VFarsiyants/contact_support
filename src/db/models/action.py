from datetime import date as db_date

from sqlalchemy import String, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Action(Base):
    """Actions"""
    __tablename__ = "action"

    date: Mapped[db_date] = mapped_column(Date(), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    every_year: Mapped[bool] = mapped_column(Boolean)
