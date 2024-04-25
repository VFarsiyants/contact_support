from datetime import date

from sqlalchemy import String, Text, Date
from sqlalchemy import Enum as DbEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.base import Base
from src.repositories.enums import ContactLevelEnum, enum_values


class Contact(Base):
    """Contacts"""
    __tablename__ = "contact"

    fullname: Mapped[str] = mapped_column(
        String(150), nullable=False, index=True)
    birthdate: Mapped[date] = mapped_column(Date(), nullable=False)
    phone: Mapped[str] = mapped_column(String(150), nullable=False)
    level: Mapped[str] = mapped_column(
        DbEnum(ContactLevelEnum,
               name='contact_level',
               nullable=False,
               values_callable=enum_values))
    city: Mapped[str] = mapped_column(String(150), nullable=False)
    additional_info: Mapped[str] = mapped_column(Text())

    # In URS said it's should be selection of choices 
    # but this choices were not given, so we use just text type here
    profession: Mapped[str] = mapped_column(
        String(150), nullable=False, index=True)
