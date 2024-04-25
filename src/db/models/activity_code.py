from datetime import date as db_date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ActivityCode(Base):
    """Activity codes"""
    __tablename__ = "activity_code"

    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    date: Mapped[db_date] = mapped_column(Date(), nullable=False)
